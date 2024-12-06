from rest_framework import serializers
from .models import Order, OrderItem, Product, Category

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent",
            "subcategories",
            "products",
            # "parent_v2",
            # "subcategories_v2",
        )

    class NestedProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "price", "stock", "status")

    products = NestedProductSerializer(many=True, read_only=True)

    class ParentCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ("id", "name")

    parent = ParentCategorySerializer(read_only=True)

    class SubcategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ("id", "name")

    subcategories = SubcategorySerializer(many=True, read_only=True)

    # subcategories_v2 = serializers.SerializerMethodField()

    # def get_subcategories_v2(self, obj):
    #     """Recursively serialize subcategories."""
    #     subcategories = obj.subcategories.all()
    #     return CategorySerializer(subcategories, many=True).data

    # parent_v2 = serializers.SerializerMethodField()

    # def get_parent_v2(self, obj):
    #     """Serialize the parent object."""
    #     parent = obj.parent
    #     if parent:
    #         return {"id": parent.id, "name": parent.name}


class BaseProductSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """Reusable validation method for product data."""
        errors = {}

        # Ensure stock is valid when the status is active
        if data["status"] == Product.Status.ACTIVE and data["stock"] <= 0:
            errors["status"] = "Active products must have a stock greater than zero."

        # Ensure price is within a reasonable range
        if data["price"] <= 0 or data["price"] > 99999999.00:
            errors["price"] = (
                "Price must be greater than 0 and less than 99,999,999.00."
            )

        # Ensure the category is assigned and exists
        category_data = data.get("category")
        if not category_data:
            errors["category"] = "Category must be provided and cannot be null."
        else:
            category_id = category_data.get("id")
            if not category_id:
                errors["category"] = "Category ID must be provided."
            elif not Category.objects.filter(id=category_id).exists():
                errors["category"] = "The specified category does not exist."

        # Ensure product name length is reasonable
        if len(data["name"]) > 255:
            errors["name"] = "Product name must not exceed 255 characters."

        # Ensure description length is within a limit
        if "description" in data and len(data["description"]) > 1000:
            errors["description"] = "Description must not exceed 1000 characters."

        # If there are any errors, raise them all at once
        print(errors)
        if errors:
            raise serializers.ValidationError(errors)

        return data


class ProductSerializer(BaseProductSerializer):
    class CategorySerializer1(serializers.ModelSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField(read_only=True)

        class Meta:
            model = Category
            fields = ["id", "name"]

    category = CategorySerializer1()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "status",
            "category",
        ]
        read_only_fields = [
            "total_units_sold",
            "total_revenue",
            "total_orders",
            "average_quantity_per_order",
            "days_since_last_sale",
            "peak_sales_day",
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("category", None)
        category_id = category_data["id"]
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product


class OrderListCreateSerializer(serializers.ModelSerializer):
    class OrderItemListCreateSerializer(serializers.ModelSerializer):
        class NestedOrderProductSerializer(serializers.ModelSerializer):
            id = serializers.UUIDField()
            name = serializers.CharField(read_only=True)
            price = serializers.DecimalField(
                max_digits=10, decimal_places=2, read_only=True
            )

            class Meta:
                model = Product
                fields = [
                    "id",
                    "name",
                    "price",
                ]

        product = NestedOrderProductSerializer()
        # FLATTENING NESTED PRODUCT FIELDS:
        # product_id = serializers.UUIDField(source="product.id")
        # product_name = serializers.CharField(source="product.name")
        # product_price = serializers.DecimalField(
        #     source="product.price", max_digits=10, decimal_places=2
        # )
        # FLATTENING NESTED PRODUCT FIELDS:

        class Meta:
            model = OrderItem
            fields = [
                "product",
                # "product_id",
                # "product_name",
                # "product_price",
                "quantity",
                "item_subtotal",
            ]

    class OrderNestedUserSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField()
        email = serializers.EmailField(read_only=True)
        first_name = serializers.CharField(read_only=True)
        last_name = serializers.CharField(read_only=True)

        class Meta:
            model = User
            fields = ["id", "email", "first_name", "last_name"]

    user = OrderNestedUserSerializer()

    order_items = OrderItemListCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",  # forward relation
            "shipping_address",
            "status",
            "total_price",
            "created_at",
            "updated_at",
            "order_items",  #
            # "ordered_products",
        ]

    def validate(self, data):
        """Perform cross-field validation for all fields."""

        # Extract user and order items
        user_data = data.get("user")
        order_items_data = data.get("order_items")

        # Validate user data
        if not user_data or not user_data.get("id"):
            raise serializers.ValidationError(
                {"user": "Valid User information is required."}
            )

        user = User.objects.filter(id=user_data["id"]).first()
        if not user:
            raise serializers.ValidationError(
                {"user": "User with the provided email does not exist."}
            )

        # Validate order items
        if not order_items_data:
            raise serializers.ValidationError(
                {"order_items": "At least one order item is required."}
            )

        # Check each order item
        for item_data in order_items_data:
            product_id = item_data["product"]["id"]
            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise serializers.ValidationError(
                    {"order_items": f"Product with ID {product_id} does not exist."}
                )

            # check if quantity is zero
            quantity = item_data["quantity"]
            if quantity == 0:
                raise serializers.ValidationError(
                    {
                        "order_items": f"Quantity for product `{product.name}` cannot be zero."
                    }
                )

            # check if quantity is greater than stock
            if product.stock < quantity:
                raise serializers.ValidationError(
                    {"order_items": f"Insufficient stock for product `{product.name}`."}
                )

            # Check if the product is inactive
            if product.status == Product.Status.INACTIVE:
                raise serializers.ValidationError(
                    {"order_items": f"Product `{product.name}` is inactive."}
                )

        return data

    def create(self, validated_data):
        """Create order with validated data."""

        # Extract user and order items from validated data
        user_data = validated_data.pop("user")
        order_items_data = validated_data.pop("order_items")

        # Create the order
        user = User.objects.get(id=user_data["id"])
        order = Order.objects.create(user=user, **validated_data)

        # Create order items and reduce stock for each product
        for item_data in order_items_data:
            product = Product.objects.get(id=item_data["product"]["id"])
            quantity = item_data["quantity"]

            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            product.reduce_stock(quantity)  # Decrease stock after adding to order

        return order


class OrderRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class OrderItemSerializer(serializers.ModelSerializer):
        class NestedProductSerializer(serializers.ModelSerializer):
            class Meta:
                model = Product
                fields = ["id", "name", "price"]

        product = NestedProductSerializer()

        class Meta:
            model = OrderItem
            fields = ["product", "quantity", "item_subtotal"]

    class UserSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField()
        email = serializers.EmailField(read_only=True)
        first_name = serializers.CharField(read_only=True)
        last_name = serializers.CharField(read_only=True)

        class Meta:
            model = User
            fields = ["id", "email", "first_name", "last_name"]

    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shipping_address",
            "status",
            "total_price",
            "created_at",
            "updated_at",
            "order_items",
        ]


class ProductRetrieveUpdateDestroySerializer(BaseProductSerializer):
    class CategoryRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField(read_only=True)

        class Meta:
            model = Category
            fields = ["id", "name"]

    category = CategoryRetrieveUpdateDestroySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "status",
            "category",
        ]
        read_only_fields = [
            "total_units_sold",
            "total_revenue",
            "total_orders",
            "average_quantity_per_order",
            "days_since_last_sale",
            "peak_sales_day",
        ]

    def update(self, instance, validated_data):
        # Extract category dict form request bod and add back category instance
        category_data = validated_data.pop("category", None)
        if category_data and isinstance(category_data, dict):
            category = Category.objects.get(id=category_data["id"])
            validated_data["category"] = category

        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
