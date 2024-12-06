from faker import Faker
import faker_commerce


from ..models import (
    Category,
    OrderItem,
    Product,
    Order,
    Cart,
    CartItem,
    Review,
    ContentType,
)
import random
from django.contrib.auth import get_user_model

User = get_user_model()


def run():
    fake = Faker()
    fake.add_provider(faker_commerce.Provider)

    # Seed Categories and Products
    print("Deleting old data....")
    Review.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    users = User.objects.exclude(email="adminme@gmail.com")
    # Delete all users except adminme
    for user in users:
        user.delete()

    # return

    print("Populating new data.....")

    # Seed Categories
    categories_data = [
        {"name": "Electronics"},
        {"name": "Smartphones"},
        {"name": "Laptops"},
        {"name": "Home Appliances"},
    ]

    for cat in categories_data:
        Category.objects.create(**cat)

    cat1 = Category.objects.get(name="Electronics")
    cat2 = Category.objects.get(name="Smartphones")
    cat2.parent = cat1
    cat2.save()

    categories = Category.objects.all()

    # Seed Products
    for _ in range(10):
        try:
            product = Product()
            product.name = fake.ecommerce_name()
            product.description = fake.sentence(nb_words=20)
            product.price = fake.pydecimal(
                left_digits=5,
                right_digits=2,
                min_value=1,
                max_value=10000,
                positive=True,
            )
            product.status = fake.random.choice(
                [Product.Status.ACTIVE, Product.Status.INACTIVE]
            )
            product.stock = fake.random_int(min=1, max=20)
            product.category = random.choice(categories)  # Adding random category
            product.save()
            print(f"Saved Product: {product.name}")
        except Exception as e:
            print(f"Error saving product: {e}")

    # Seed Users
    print("Seeding Users...")
    for _ in range(5):  # Create 20 users
        user = User.objects.create_user(
            email=fake.email(),
            password="password123",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        print(f"Created User: {user.email}")

    # Seeding Orders
    print("Seeding Orders...")
    for _ in range(3):  # Create 3 orders
        user = random.choice(User.objects.exclude(email="adminme@gmail.com"))
        order = Order.objects.create(
            user=user,
            status=random.choice([Order.Status.PENDING, Order.Status.SHIPPED]),
        )

        # Add products to the order
        for _ in range(random.randint(1, 5)):
            product = random.choice(Product.objects.all())
            quantity = random.randint(1, 3)  # Random quantity between 1 and 3
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        # Calculate total price for the order
        print(f"Created Order {order.id} for User {user.email}")

    # Seeding Carts
    print("Seeding Carts...")
    for user in User.objects.exclude(email="adminme@gmail.com"):
        cart = Cart.objects.create(
            user=user, status=random.choice([Cart.Status.ACTIVE, Cart.Status.ABANDONED])
        )

        # Add products to the cart
        for _ in range(random.randint(1, 5)):
            product = random.choice(Product.objects.all())
            quantity = random.randint(1, 3)  # Random quantity between 1 and 3
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        print(f"Created Cart for User {user.email}")

    # Seeding Reviews
    print("Seeding Reviews...")
    for product in Product.objects.all():
        for _ in range(random.randint(1, 3)):
            user = random.choice(User.objects.exclude(email="adminme@gmail.com"))
            Review.objects.create(
                user=user,
                content_type=ContentType.objects.get_for_model(
                    Product
                ),  # Link review to Product
                object_id=product.id,
                text=fake.sentence(nb_words=20),
                rating=fake.random_int(1, 5),
            )
            print(f"Created Review for Product {product.name} by {user.email}")

    print("Seeding complete!")
