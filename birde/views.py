from django.shortcuts import render

from birde.models import Message,Connection,User
import pop_client


def index(request):
    con_details=Connection.objects.get(user_id=User.objects.get(username="root"))
    message,socket=pop_client.connect_to_server(con_details.popHost,con_details.popPort,con_details.popUser,con_details.popPass)
    message_list=pop_client.return_latest_messages(socket,message)
    print message_list
    #message_list = Message.objects.order_by('-dateSent')[:5]
    context = {'message_list': message_list}
    return render(request, 'index.html', context)