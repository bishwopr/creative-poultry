from django.db import models
from account.models import User
import json

class Category(models.Model):
    category = models.CharField(max_length=55, null=False)

    def __str__(self):
        return self.category

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    desc = models.TextField(null=False)
    price = models.IntegerField(default=0, null=False)
    discount = models.IntegerField(default=0, null=False)
    image = models.ImageField(upload_to='product_images', null=False)
   
    def to_json(self):
        data = {
            'name': self.name,
            'price': str(self.price),
            'desc': self.desc,
        }
        return json.dumps(data)
