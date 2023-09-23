from django.urls import path
from .views import ProfileView, InformationUpdateView,sales_chart
app_name = 'business'
urlpatterns = [
    path('',ProfileView.as_view(),name='profile'),
    path('info-update',InformationUpdateView.as_view(),name='info-update'),
    path('sales-chart',sales_chart, name='sales_chart')
]
