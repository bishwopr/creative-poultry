# Generated by Django 4.1.7 on 2023-08-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_shipping_charge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_charge',
        ),
        migrations.AddField(
            model_name='order',
            name='shippingcharge',
            field=models.IntegerField(default=0, null=True),
        ),
    ]