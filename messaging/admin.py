from django.contrib import admin
from .models import Message, MessageRoom

admin.site.register(Message)
admin.site.register(MessageRoom)