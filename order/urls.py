from django.urls import path
from .views import *
app_name = 'order'
urlpatterns = [
    path('checkout',checkout,name='checkout'),
    path('<id>/details',orderDetail,name='details'),
    path('your-orders',userOrders,name='user-orders'),
    path('business-orders',businessOrders,name='business-orders'),
    path('<id>/deny',denyOrder,name='deny-order'),
    path('validate-promo',validate_promo_code,name='validate-promo'),

]
