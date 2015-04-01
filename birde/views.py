from django.shortcuts import render

from birde.models import Message


def index(request):
    message_list = Message.objects.order_by('-dateSent')[:5]
    context = {'message_list': message_list}
    return render(request, 'index.html', context)