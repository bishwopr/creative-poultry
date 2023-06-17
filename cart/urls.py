from django.urls import path
from .views import CartHomeView, AddToCart
app_name = 'cart'

urlpatterns = [
    path('',CartHomeView.as_view(), name='home'),
    path('<pk>/addtobasket',AddToCart.as_view(), name='add'),
]
