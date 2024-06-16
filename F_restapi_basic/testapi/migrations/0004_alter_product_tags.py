# Generated by Django 4.2.13 on 2024-06-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapi", "0003_tag_product_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="products", to="testapi.tag"
            ),
        ),
    ]