from faker import Faker
from htmx.models import Category, Product, Option, Attribute, ProductVariant, VariantOption, VariantAttribute
import random
import os

data = [
    {
        "category": "Smartphones",
        "options": {
            "Color": ["Black", "White", "Blue"],
            "Storage": ["64GB", "128GB", "256GB", "512GB", "1TB"],
            "RAM": ["4GB", "6GB", "8GB", "12GB"],
            "Condition": ["New", "Used"],
            "Display": ["5.5 inch", "6 inch", "6.5 inch", "7 inch"],
            "Network": ["4G", "5G"],
            "OS": ["Android", "iOS"],
        },
        "products": ["iPhone 13 Pro", "Samsung Galaxy S21 Ultra", "Google Pixel 6 Pro", "OnePlus 9 Pro", "Xiaomi Mi 11"]
    },
    {
        "category": "Laptops",
        "options": {
            "Color": ["Black", "White", "Silver"],
            "Storage": ["128GB", "256GB", "512GB", "1TB", "2TB"],
            "RAM": ["4GB", "8GB", "16GB", "32GB", "64GB"],
            "Condition": ["New", "Used"],
            "Display": ["13 inch", "15 inch", "17 inch"],
            "OS": ["Windows", "macOS", "Linux"],
        },
        "products": ["MacBook Pro", "Dell XPS 15", "Lenovo ThinkPad X1 Carbon", "HP Spectre x360", "Asus ROG Zephyrus G14"]
    },
    {
        "category": "Clothing",
        "options": {
            "Color": ["Black", "White", "Blue", "Red", "Green", "Yellow"],
            "Size": ["XS", "S", "M", "L", "XL", "XXL"],
            "Style": ["Casual", "Formal", "Sportswear", "Traditional", "Western"],
            "Material": ["Cotton", "Polyester", "Wool", "Silk", "Denim", "Leather"],
        },
        "products": ["Nike Dri-FIT T-shirt", "Adidas Originals Hoodie", "Levi's 501 Jeans", "Ralph Lauren Polo Shirt", "H&M Slim Fit Chinos"]
    },
    {
        "category": "Home & Kitchen",
        "options": {
            "Color": ["Black", "White", "Blue", "Red", "Green", "Yellow"],
            "Material": ["Plastic", "Wood", "Metal", "Glass", "Ceramic"],
            "Dimensions": ["Small", "Medium", "Large"],
            "Condition": ["New", "Used"],
        },
        "products": ["Instant Pot Duo", "Nespresso Vertuo Coffee Maker", "IKEA Kallax Shelf Unit", "Dyson V11 Vacuum Cleaner", "Cuisinart Stainless Steel Cookware Set"]
    }
]


def run():
    Category.objects.all().delete()
    Product.objects.all().delete()
    Option.objects.all().delete()
    Attribute.objects.all().delete()
    ProductVariant.objects.all().delete()
    VariantOption.objects.all().delete()
    VariantAttribute.objects.all().delete()

    n = 1
    fake = Faker()

    # Create categories if they don't exist
    for category_data in data:
        category_name = category_data["category"]
        print("*" * 50)
        print(category_name)
        print("*" * 50)
        category, _ = Category.objects.get_or_create(name=category_name)

        for product_name in category_data["products"]:
            product_description = fake.text(max_nb_chars=200)
            product_price = random.uniform(10.00, 1000.00)
            product = Product.objects.create(
                name=product_name,
                description=product_description,
                price=product_price,
                category=category,
            )

            # Create a base variant with random SKU, price, and stock
            base_variant_sku = fake.ean13()  # Generate unique SKU
            base_variant_price = random.uniform(product_price * 0.9, product_price * 1.1)
            base_variant_stock = random.randint(10, 100)
            base_variant = ProductVariant.objects.create(
                product=product,
                sku=base_variant_sku,
                price=base_variant_price,
                stock=base_variant_stock,
            )
            print(base_variant.variant_name())

            # Create additional variants with random options
            for _ in range(random.randint(1, len(category_data["options"]))):
                variant = ProductVariant.objects.create(
                    product=product,
                    sku=fake.ean13(),
                    price=base_variant_price + random.uniform(10.00, 100.00),
                    stock=base_variant_stock,  # Keep base stock for now
                )
                for option_name, option_values in category_data["options"].items():
                    option_value = random.choice(option_values)
                    VariantOption.objects.create(
                        variant=variant,
                        option=Option.objects.get_or_create(name=option_name, category=category)[0],
                        value=option_value,
                    )
                print(variant.variant_name())
