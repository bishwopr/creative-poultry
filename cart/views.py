from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.shortcuts import render
from product.models import Product
from cart.models import Cart, CartItem

class CartHomeView(View):
    def get(self, request):
        cart = getUserCart(request.user)
        cartitems = CartItem.objects.filter(cart=cart).order_by('-id')
        return render(request, 'cart/home.html', {'cart': cart, 'cartitems': cartitems})

def getUserCart(user):
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        cart = Cart.objects.create(user=user)
    return cart

class AddToCart(View):
    def get(self, request, pk):
        cart = getUserCart(request.user)
        product = get_object_or_404(Product, id=pk)
        if product.stock_quantity < 1:
            messages.success(request, 'Seems like the product is out of stock for now.')
        elif not CartItem.objects.filter(cart=cart, product=product).exists():
            CartItem.objects.create(cart=cart, product=product)
            messages.success(request, 'Product added to your cart.')
        else:
            # cart_item = CartItem.objects.get(cart=cart, product=product)
            # cart_item.quantity += 1
            # cart_item.save()
            messages.success(request, 'Product already in your cart.')
        return redirect('product:detail', pk=pk)


def cartHandler(request):
    action =request.GET['action']
    cartitem_id =request.GET['ciid']
    cp = CartItem.objects.get(id=cartitem_id)
    if action == 'plus':
        if cp.quantity < cp.product.stock_quantity:
            cp.quantity += 1
            cp.save()
        else:
            messages.error(request, 'Quantity exceeds available stock.')
    elif action == 'minus' and cp.quantity>1:
        cp.quantity -=1
        cp.save()
    elif action == 'remove':
        cp.delete()
        messages.success(request, 'Product removed from your cart.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

