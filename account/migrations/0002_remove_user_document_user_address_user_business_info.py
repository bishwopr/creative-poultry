# Generated by Django 4.1.7 on 2023-05-21 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='document',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='business_info',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
