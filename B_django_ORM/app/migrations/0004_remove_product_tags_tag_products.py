# Generated by Django 4.2.9 on 2024-01-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_product_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="tags",
        ),
        migrations.AddField(
            model_name="tag",
            name="products",
            field=models.ManyToManyField(related_name="tags", to="app.product"),
        ),
    ]
