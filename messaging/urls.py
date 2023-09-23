from django.urls import path
from messaging.views import check_message_room, view_messages, message_room, send_messages
app_name = 'messaging'

urlpatterns = [
    path('send_message/<int:product_id>/', check_message_room, name='check_message_room'),
    path('message-room/<int:id>', message_room, name='message-room'),
    path('view_messages/', view_messages, name='view_messages'),
    path('send_messages/', send_messages, name='send_messages'),
]
