from django.db import models
from account.models import User
from product.models import Product
from django.db.models import Count, Q


class MessageRoom(models.Model):
    sender = models.ForeignKey(User, related_name='sender_rooms', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_rooms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender.username} - {self.receiver.username}"
    
    @property
    def messages(self):
        return Message.objects.filter(room=self.id)
    
    @classmethod
    def with_messages(cls, user):
        return cls.objects.annotate(message_count=Count('message')).filter(
            Q(sender=user) | Q(receiver=user),
            message_count__gt=0
        ).order_by('-id')


class Message(models.Model):
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"
