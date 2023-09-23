from django.urls import path
from .views import CustomerRegisterView, BusinessRegisterView, SigninView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name ='account'
urlpatterns = [
    path('register',CustomerRegisterView.as_view() ,name='register'),
    path('business-register',BusinessRegisterView.as_view() ,name='business-register'),
    path('',SigninView.as_view() ,name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'), 
    path('delete-account/', views.delete_account, name='delete-account'),
]
