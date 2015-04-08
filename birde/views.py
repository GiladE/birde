from django.shortcuts import render
from birde.models import Message,Connection,User
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


import pop_client


def index(request):
    con_details=Connection.objects.get(user_id=User.objects.get(username="root"))
    message,socket=pop_client.connect_to_server(con_details.popHost,con_details.popPort,con_details.popUser,con_details.popPass)
    message_list=pop_client.return_latest_messages(socket,message)
    #message_list = Message.objects.order_by('-dateSent')[:5]
    context = {'message_list': message_list}
    return render(request, 'index.html', context)

@csrf_exempt
def send(request):
	msgTo = request.POST.get('email')
	msgSubject = request.POST.get('subject')
	msgBody = request.POST.get('message')
	response_data={"response":"250"}
	return HttpResponse(json.dumps(response_data),content_type='application/json')