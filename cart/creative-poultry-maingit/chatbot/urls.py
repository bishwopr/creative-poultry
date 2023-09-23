from django.urls import path
from .views import ask_bot

urlpatterns = [
    # Other URL patterns in your project
    path('', ask_bot, name='chatbot'),
]
