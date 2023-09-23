from django.urls import path
from .views import CartHomeView, AddToCart, cartHandler



app_name = 'cart'

urlpatterns = [
    path('home/', CartHomeView.as_view(), name='home'),
    path('<pk>/addtobasket',AddToCart.as_view(), name='add'), 
    path('cart-action', cartHandler, name='carthandler'),
]
