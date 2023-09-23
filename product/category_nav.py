from .models import Category
from cart.models import Cart, CartItem
def navbar(request):
    cartcount =0
    if not request.user.is_anonymous and request.user.is_customer :
        cart = Cart.objects.get(user=request.user)
        cartcount = CartItem.objects.filter(cart=cart).count()


    cats = Category.objects.all()
    return {'categories': cats,'cartcount':cartcount}