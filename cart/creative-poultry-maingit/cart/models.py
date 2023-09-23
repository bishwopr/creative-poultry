from django.db import models
from product.models import Product
from account.models import User
from django.utils import timezone

class Cart(models.Model):
    date_joined = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    
    @property
    def get_total(self):
        total = sum(item.totalprice for item in CartItem.objects.filter(cart=self.id))
        return str(round(total))
    
    @property
    def get_total_quantity(self):
        total = sum(item.quantity for item in CartItem.objects.filter(cart=self.id))
        return str(round(total))
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name
    
    @property
    def totalprice(self):
        return (self.product.price*self.quantity)