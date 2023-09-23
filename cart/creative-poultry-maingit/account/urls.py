from django.urls import path
from .views import CustomerRegisterView, BusinessRegisterView, SigninView
from django.contrib.auth import views as auth_views

app_name ='account'
urlpatterns = [
    path('',CustomerRegisterView.as_view() ,name='register'),
    path('business-register',BusinessRegisterView.as_view() ,name='business-register'),
    path('login',SigninView.as_view() ,name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),  
    path('reset-password/',auth_views.PasswordChangeView.as_view(
            template_name='account/reset-password.html',
            success_url = '/logout',
       
        ),
        name='reset_password'
    )
]
