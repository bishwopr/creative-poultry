from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    directions = models.TextField()
    link = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    ner = models.TextField()

    def __str__(self):
        return self.title
