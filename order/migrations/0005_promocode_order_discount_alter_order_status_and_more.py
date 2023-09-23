# Generated by Django 4.1.7 on 2023-09-03 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_order_shipping_charge_order_shippingcharge'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expiry_date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Processed', 'Processed'), ('Shipped', 'Shipped'), ('Denied', 'Denied'), ('Cancelled', 'Cancelled')], default='Submitted', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.promocode'),
        ),
    ]