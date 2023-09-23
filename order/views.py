from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem, PromoCode
from .forms import ShippingForm, PromoCodeForm
from product.models import Product





@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    promo_code_discount = request.session.pop('promo_code_discount', 0)
    promo_code = request.session.get('promo_code')
    
    cartproducts = CartItem.objects.filter(cart=cart)
    # print('promo_code_discount',promo_code_discount,promo_code)
    if not cartproducts.first():
        messages.error(request, "Your cart is empty.")
        return redirect('/basket/home/')

    if request.method == 'POST':
        form = ShippingForm(request.POST)

        if form.is_valid():
            
            try:
                if  promo_code is not None:
                    promo_code = PromoCode.objects.get(pk=promo_code)
                    order = Order.objects.create(
                        user=request.user,
                        total_price=cart.get_total,
                        address=form.cleaned_data['address'],
                        phone=form.cleaned_data['phone'],
                        payment_method=form.cleaned_data['payment_method'],
                        promo_code=promo_code
                    )
                    order.save()
                    order_items = [OrderItem(order=order, product=i.product, quantity=i.quantity, price=i.product.price) for i in cartproducts]
                    OrderItem.objects.bulk_create(order_items)
                    del request.session['promo_code']
                else:
                    order = Order.objects.create(
                        user=request.user,
                        total_price=cart.get_total,
                        address=form.cleaned_data['address'],
                        phone=form.cleaned_data['phone'],
                        payment_method=form.cleaned_data['payment_method']
                    )
                    order.save()
                    order_items = [OrderItem(order=order, product=i.product, quantity=i.quantity, price=i.product.price) for i in cartproducts]
                    OrderItem.objects.bulk_create(order_items)
                
                # Update stock_quantity for each product in cartproducts
                for cart_item in cartproducts:
                    product = cart_item.product
                    ordered_quantity = cart_item.quantity

                    # Ensure stock_quantity is not negative
                    new_stock_quantity = product.stock_quantity - ordered_quantity
                    product.stock_quantity = max(new_stock_quantity, 0)  # Ensure non-negative value
                    product.save()
                cartproducts.delete()
                
                messages.success(request,'Order submitted successfully. Check #{} for more info.'.format(order.id))
                return redirect('/order/your-orders')
            except Exception as e:
                print("An error occurred:", e)
                if order:
                    order.delete()
    
    
    form = ShippingForm()
    form1=PromoCodeForm()
    context = {'cart': cart,'cartitems':cartproducts,'form': form,'form1': form1, 'promo_code_discount':promo_code_discount}
    return render(request, 'order/checkout.html', context)


def userOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'order/user-orders.html',{'orders':orders})

def businessOrders(request):
    products = Product.objects.filter(creator=request.user).order_by('-id')
    orders = Order.objects.filter(orderitem__product__in=products).distinct().order_by('-id')
    return render(request, 'order/business-orders.html',{'orders':orders})

def orderDetail(request,id):
    order = Order.objects.get(id=id)
    orderitems = OrderItem.objects.filter(order=order)
    if request.method == 'POST':
        shippingcharge = request.POST.get('shippingcharge')
        order.status= 'Processed'
        order.shippingcharge= shippingcharge
        order.save()
        messages.success(request,'You approved the order.')
        return redirect('/order/business-orders')
    return render(request, 'order/order-detail.html',{'order':order,'orderitems':orderitems})

@login_required
def denyOrder(request,id):
    if request.user.is_business:
        order = Order.objects.get(id=id)
        order.status= 'Denied'
        order.save()
        messages.success(request,'You denied the order.')
        return redirect('/order/business-orders')
    else:
        return HttpResponse('403- Not Authorized')



def validate_promo_code(request):
    if request.method == 'POST':
        promo_code_form = PromoCodeForm(request.POST)
        if promo_code_form.is_valid():
            code = promo_code_form.cleaned_data['code']
            try :
                promo_code = PromoCode.objects.get(code=code, expiry_date__gte=timezone.now())
                if Order.objects.filter(user=request.user, promo_code=promo_code).exists():
                    messages.error(request, 'The code has already been used in your previous orders.')
                    return redirect('order:checkout')
                messages.success(request, 'PromoCode is Validated and you will have {} % off on your overall order. Enjoy!!'.format(promo_code.discount_percentage))
                request.session['promo_code_discount'] = promo_code.discount_percentage
                request.session['promo_code'] = promo_code.id
                return redirect('order:checkout')
            except PromoCode.DoesNotExist:
                messages.error(request, 'Code is either expired or does not exist at all.')
                return redirect('order:checkout')
        else:
            pass
    else:
        promo_code_form = PromoCodeForm()
    return HttpResponseRedirect('something went wrong.')