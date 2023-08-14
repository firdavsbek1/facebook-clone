import datetime
from django.shortcuts import render
from accounts.models import CustomUser
from messages_app.forms import MessageForm
from messages_app.models import Message
from django.db.models import Q


# Create your views here.
def message(request, user_id):
    to_user = CustomUser.objects.get(id=user_id)

    if request.method=='POST':
        form=MessageForm(data=request.POST)
        if form.is_valid():
            message_instance=form.save(commit=False)
            message_instance.message_sender=request.user
            message_instance.message_receiver=to_user
            to_user.last_message_time=datetime.datetime.now()
            to_user.save()
            request.user.last_message_time=datetime.datetime.now()
            request.user.save()
            message_instance.save()
    messages = Message.objects.filter(
        Q(message_sender=request.user, message_receiver=to_user) |
        Q(message_sender=to_user, message_receiver=request.user)
    ).order_by('created_time')
    messages.update(is_owner=False)
    messages.filter(message_sender=request.user).update(is_owner=True)
    context = {
        'messages': messages,
        'to_user':to_user,
        'current_user':request.user,
        'friends':CustomUser.objects.get(
            id=request.user.id).friend_list.friends.all().order_by('-last_message_time')
    }

    return render(request, 'messages_app/message.html',context)
