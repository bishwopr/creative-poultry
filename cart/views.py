from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .models import Cart, CartItem
from django.contrib import messages
from product.models import Product

class CartHomeView(TemplateView):
    template_name = 'cart/home.html'

    def get_context_data(self, **kwargs):
        context = super(CartHomeView, self).get_context_data(**kwargs)
        cart = getUserCart(self.request.user)
        cartitems = CartItem.objects.filter(cart=cart).order_by('-id')
        context.update({ "cart":cart,'cartitems':cartitems})
        return context
    
def getUserCart(user):
    if  Cart.objects.filter(user = user).first():
        cart = Cart.objects.get(user = user)
    else:
        cart = Cart.objects.create(user=user)
    return cart


class AddToCart(View):
    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        cart = getUserCart(self.request.user)
        product = Product.objects.get(id=pk)
        if not CartItem.objects.filter(cart = cart, product=product).first():
            CartItem.objects.create(cart=cart, product=product)
            messages.success(self.request,'Product added to your cart.')
            return redirect('product:detail', pk=pk)
        else:
            ci=CartItem.objects.get(cart=cart,product=product)
            ci.quantity+=1
            ci.save()

            messages.success(self.request,'Product already in your cart.')
            return redirect('product:detail', pk=pk)
        

