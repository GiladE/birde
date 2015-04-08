from django.shortcuts import render
from birde.models import Message,Connection,User
from django.http import HttpResponse
import json, datetime
from django.views.decorators.csrf import csrf_exempt

import smtp_client
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
    con_details=Connection.objects.get(user_id=User.objects.get(username="root"))
    communications = smtp_client.send_mail(con_details.smtpHost,con_details.smtpPort,con_details.smtpUser,con_details.smtpPass,msgTo,msgSubject,msgBody)
    response_data={"response":communications[-1][0:3]}
    savedMsg = Message(sender=con_details.smtpUser,recipient=msgTo,dateSent=datetime.datetime.now(),subject=msgSubject,body=msgBody,type=True,owner_id=User.objects.get(username="root").id)
    savedMsg.save()
    return HttpResponse(json.dumps(response_data),content_type='application/json')