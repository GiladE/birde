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

@csrf_exempt
def chat(request):
    # Message is in the following format:
    #       user|CMND|body|CYA
    # if message is not in this format, it will be rejected
    # return json in the following format:
    #   {
    #       "code":response_code ,
    #       "response":[{sender,body,time},...] or {body,time} or {error_body,time} ,
    #       "cat": '~(=^_^)'
    #   }
    #
    # code - indicates the type of response that the server is returning
    # response - contains the payload of the reposnse whose format is dependant on the code
    # cat - Some sort of ASCII cat to offset the pain of reading an arbitrary protocol message.
    #
    # Codes:
    #   111 - Command successful, print nothing to chat window
    #   222 - Command successful, popup payload
    #   333 - Command successful, print messages to screen
    #   555 - Command unsuccessful, command failed
    #   666 - Command unsuccessful, incorrect format
    #
    message=request.POST.get('chatsend').split("|")
    response={}
    if len(message)!=4 or message[-1]!="CYA":
        response={"code":"666","response":[{"body":"Incorrect request format","time":str(datetime.datetime.now())}],"cat": "~(=^_^)"}
    else:
        if message[1]=="SEND":
            #send message
            savedChat = Message(sender="chat",recipient="chat",dateSent=datetime.datetime.now(),subject="chat",body=message[2],type=False,owner_id=User.objects.get(username=message[0]).id)
            savedChat.save()
            all_messages=[]
            raw_messages=Message.objects.all().filter(type=False)
            for msg in raw_messages:
                all_messages.append(dict({"sender":getattr(msg.owner,"username"),"body":msg.body,"time":str(msg.dateSent)}))
            response={"code":"333","response":all_messages,"cat": "~(=^_^)"}
        elif message[1]=="LOGIN":
            #join room
            print "login"
        elif message[1]=="LOGOUT":
            #leave room
            print "logout"
        elif message[1]=="RETR":
            #refresh messages on screen
            all_messages=[]
            raw_messages=Message.objects.all().filter(type=False)
            for msg in raw_messages:
                all_messages.append(dict({"sender":getattr(msg.owner,"username"),"body":msg.body,"time":str(msg.dateSent)}))
            response={"code":"333","response":all_messages,"cat": "~(=^_^)"}
            print response
        elif message[1]=="MOTD":
            #alert motd
            print "motd"
        elif message[1]=="USERS":
            #list users in room
            print "users"
        else:
            # command failed
            print "FAIL"
    return HttpResponse(json.dumps(response),content_type='application/json')