from django import template
from product.models import Product, ProductRating
from order.models import OrderItem

register = template.Library()

@register.filter(name="check_rating")
def checkrating(product, user):
    product = Product.objects.get(id=product)
    return OrderItem.objects.filter(order__user=user, order__status='Processed', product=product).exists()

@register.filter(name="check_review")
def checkreview(product, user):
    product = Product.objects.get(id=product)
    return ProductRating.objects.filter(user=user, product=product).exists()

@register.filter(name="range")
def get_range(value):
    return range(value)


@register.filter(name="render_stars")
def render_stars(rating):
    filled_stars = '<i class=" rating fa fa-star"></i>' * rating
    empty_stars = ' <i class=" erating fa fa-star"></i>' * (5 - rating)
    return f'{filled_stars}{empty_stars}'
