from django.db import models
from django.urls import reverse
from account.models import User
from business.models import BusinessInfo
import json
from django.core.validators import MaxValueValidator, MinValueValidator 

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
    stock_quantity = models.PositiveIntegerField(default=0, null=False)
   
    def to_json(self):
        data = {
            'name': self.name,
            'price': str(self.price),
            'desc': self.desc,
        }
        return json.dumps(data)
    
    def __str__(self):
        return self.name
    @property
    def mprice(self):
        return self.price + (self.price * (self.discount/100))
    @property
    def businessuser(self):
        return BusinessInfo.objects.get(user = self.creator)
    
    @property
    def average_rating(self):
        ratings = self.product_ratings.all()
        if ratings:
            total_ratings = sum([rating.rating for rating in ratings])
            return int(total_ratings / len(ratings))
        return 0
    
    @property
    def user_reviews(self):
        return self.product_ratings.all()
    
    def get_absolute_url(self):
        return reverse('product:detail', args=[str(self.pk)])
        

class ProductRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()

    
    
