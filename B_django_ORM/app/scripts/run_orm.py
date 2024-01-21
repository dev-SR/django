from app.models import Product, Tag
from pprint import pprint


def run(*arg):
    products = Product.objects.all()
    for product in products:
        tags = product.tags.all()
        pprint({"name": product.title, "tags": list(tags)})
    # print(list(products))

    tag1 = Tag.objects.get(pk=1)
    tag1_products = tag1.products.all()
    pprint(list(tag1_products))
