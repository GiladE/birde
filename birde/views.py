from django.shortcuts import render
from birde.models import Message,Connection,User
from django.http import HttpResponse
from django.shortcuts import redirect
import json, datetime
from django.views.decorators.csrf import csrf_exempt

import smtp_client
import pop_client


def index(request):
    currentUser = request.GET.get('user')
    if currentUser==None:
        currentUser="root"
    con_details=Connection.objects.get(user_id=User.objects.get(username=currentUser))
    message,socket=pop_client.connect_to_server(con_details.popHost,con_details.popPort,con_details.popUser,con_details.popPass)
    message_list=pop_client.return_latest_messages(socket,message)
    sent_list=Message.objects.all().filter(owner=User.objects.get(username=currentUser))
    user_list=User.objects.all();
    context = {'message_list': message_list, "sent_list":sent_list,"user_list":user_list,"current_user":currentUser,"current_settings":con_details}
    return render(request, 'index.html', context)

@csrf_exempt
def send(request):
    msgTo = request.POST.get('email')
    msgSubject = request.POST.get('subject')
    msgBody = request.POST.get('message')
    user=request.POST.get('user')
    con_details=Connection.objects.get(user_id=User.objects.get(username=user))
    communications = smtp_client.send_mail(con_details.smtpHost,con_details.smtpPort,con_details.smtpUser,con_details.smtpPass,msgTo,msgSubject,msgBody)
    response_data={"response":communications[-1][0:3]}
    savedMsg = Message(sender=con_details.smtpUser,recipient=msgTo,dateSent=datetime.datetime.now(),subject=msgSubject,body=msgBody,type=True,owner_id=User.objects.get(username="root").id)
    savedMsg.save()
    return HttpResponse(json.dumps(response_data),content_type='application/json')


@csrf_exempt
def settings(request):
    user=request.POST.get('user')
    popHost=request.POST.get('popHost')
    popPort=request.POST.get('popPort')
    popUser=request.POST.get('popUser')
    popPass=request.POST.get('popPass')
    smtpHost=request.POST.get('smtpHost')
    smtpPort=request.POST.get('smtpPort')
    smtpUser=request.POST.get('smtpUser')
    smtpPass=request.POST.get('smtpPass')
    con_details=Connection.objects.get(user_id=User.objects.get(username=user))
    con_details.popHost=popHost
    con_details.popPort=popPort
    con_details.popUser=popUser
    con_details.popPass=popPass
    con_details.smtpHost=smtpHost
    con_details.smtpPort=smtpPort
    con_details.smtpUser=smtpUser
    con_details.smtpPass=smtpPass
    con_details.save()
    response_data={"response":str([popHost,popPort,popUser,popPass,smtpHost,smtpPort,smtpUser,smtpPass])}
    return HttpResponse(json.dumps(response_data),content_type='application/json')

@csrf_exempt
def delete(request):
    user=request.POST.get('user')
    con_details=Connection.objects.get(user_id=User.objects.get(username=user))
    message,socket=pop_client.connect_to_server(con_details.popHost,con_details.popPort,con_details.popUser,con_details.popPass)
    delMsg = pop_client.delete_message(socket,message,request.POST.get('msgnum'))
    return HttpResponse(json.dumps({"response":"deleted!!!"}),content_type='application/json')