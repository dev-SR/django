# Generated by Django 4.2.10 on 2024-02-14 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("htmx", "0002_alter_product_description"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="variantoption",
            unique_together={("variant", "option", "value")},
        ),
    ]
