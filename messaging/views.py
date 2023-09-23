from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from account.models import User
from product.models import Product
from .models import Message, MessageRoom


@login_required
def check_message_room(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    receiver = product.creator
    sender = request.user
    message_room = MessageRoom.objects.filter(product=product,sender=sender)
    if not message_room.exists():
        message_room =MessageRoom.objects.create(product=product,sender=sender, receiver=receiver)
    else:
        message_room = MessageRoom.objects.get(product=product,sender=sender)
        


    # if request.method == 'POST':
    #     content = request.POST.get('content')
    #     sender = request.user

    #     message = Message.objects.create(
    #         sender=sender,
    #         receiver=receiver,
    #         product=product,
    #         content=content
    #     )

        # Perform any additional actions, notifications, or redirects

    return redirect('messaging:message-room',id=message_room.id)
    

@login_required
def message_room(request,id):
    
    message_room = get_object_or_404(MessageRoom, id=id)
    if request.user == message_room.sender or request.user == message_room.receiver:
        return render(request, 'messaging/messageroom.html', {'message_room':message_room})
    
    else:
        return HttpResponse('Unauthorized access. Sorry')


def view_messages(request):
    # messages = MessageRoom.objects.filter(receiver=user).order_by('-id') | MessageRoom.objects.filter(sender=user).order_by('-id')
    messages = MessageRoom.with_messages(request.user)
    return render(request, 'messaging/view_messages.html', {'messages': messages})

@login_required
def send_messages(request):
    if request.method == "POST":
        message = request.POST.get('message')
        room_id = request.POST.get("roomid")
        room = MessageRoom.objects.get(id=room_id)
        Message.objects.create(room=room,content=message, sender=request.user)
        return redirect('messaging:message-room',id=room.id)
    
    return HttpResponse('Something went wrong.')
        


        
