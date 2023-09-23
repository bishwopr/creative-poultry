from .models import Category

def navbar(context):
    cats = Category.objects.all()
    return {'categories': cats}