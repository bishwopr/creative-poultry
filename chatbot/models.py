from django.db import models


class Conversation(models.Model):
    user_input = models.TextField()
    chatbot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Conversation {self.pk}"


class Query(models.Model):
    text = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
