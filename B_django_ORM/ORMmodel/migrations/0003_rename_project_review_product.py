# Generated by Django 4.0 on 2021-12-26 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ORMmodel', '0002_product_review_delete_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='project',
            new_name='product',
        ),
    ]
