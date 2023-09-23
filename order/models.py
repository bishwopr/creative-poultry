from django.db import models
from account.models import User
from product.models import Product


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.IntegerField(default=0)
    expiry_date = models.DateField()

    def __str__(self):
        return self.code

class Order(models.Model):
    ORDER_STATUSES = [('Submitted','Submitted'),
                      ('Processed','Processed'),
                      ('Shipped','Shipped'),
                      ('Denied','Denied'),
                      ('Cancelled','Cancelled'),]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length = 20, choices=ORDER_STATUSES, default='Submitted')
    shippingcharge = models.IntegerField(default=0, null=True)
    promo_code = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.DecimalField(max_digits=8, decimal_places=2, null=True)


    def __str__(self):
        return f"Order #{self.pk}"
    
    @property
    def gettotalprice(self):
        from decimal import Decimal
        if self.promo_code:
            discount_percentage = Decimal(self.promo_code.discount_percentage)
            total_price = Decimal(self.total_price)
            discounted_amount = float(total_price - (total_price * (discount_percentage / 100)))
            return discounted_amount
        return Decimal(self.total_price)
       
    
    @property
    def alltotalprice(self):
        # total = sum(int(self.total_price),int(self.shippingcharge))
        return self.gettotalprice + int(self.shippingcharge)

    
    @property
    def get_quantity(self):
        total = sum(item.quantity for item in OrderItem.objects.filter(order=self.id))
        return str(round(total))
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(null=False, default=0)

    def __str__(self):
        return str(self.order.user.username)


