# Generated by Django 4.1.7 on 2023-09-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_productrating_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
