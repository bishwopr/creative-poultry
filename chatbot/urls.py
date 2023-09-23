from django.urls import path
from chatbot.views import ask_bot

app_name = 'chatbot'
urlpatterns = [
    # Other URL patterns in your project
    path('', ask_bot, name='chatbot'),
]
