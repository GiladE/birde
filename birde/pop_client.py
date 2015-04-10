import socket
import ssl
import re
#import html2text
#METHODS FOR COMMUNICATING WITH POP SERVER:
# List:    name                   purpose
#       1: connect_to_server       : connect to POP server and verify user credentials.
#       2: return_server_status    : returns the number of messages in the mailbox as well as the size of the mailbox.
#       3: return_specific_message : returns a specific message as specified by the user.
#       4: return_latest_messages  : returns the latest 20 messages on the mailbox.
#       4: return_latest_messages  : returns the latest 10 messages on the mailbox. (if there aren't 10 messages, all messages are displayed)
#       5: return_all_messages     : returns all messages on the mailbox
#       6: delete_message          : deletes a specific message from the mailbox

# 1:
def connect_to_server(host, port, username, password):
    connection_state=True
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_clientSocket = ssl.wrap_socket(clientSocket)
    ssl_clientSocket.connect((host, port))
    data = ssl_clientSocket.read(2048)
    if data == '-ERR':
        print "Connection with server Failed!"
        connection_state = False
    else:
        ssl_clientSocket.send("user "+username+"\r\n")
        data1 = ssl_clientSocket.read(1024)
        if data1== "-ERR":
            print "Username not found!"
            connection_state=False
        else:
            ssl_clientSocket.send("pass "+password+"\r\n")
            data2 = ssl_clientSocket.read(1024)
            if data2=="-ERR":
                print "Incorrect Password"
                connection_state=False
            else:
                print "Connection to Server Successful"
                connection_state = True
    return connection_state, ssl_clientSocket


# 2:
def return_server_status(socket,connection_message):
    returning_data = ''
    if connection_message:
       	socket.send("STAT \r\n")
        #returning_data.append(ssl_client_socket.read(2048))
        data = socket.read(2048).split(" ")
        returning_data = data[1]
        # returning_data.append(re.sub('[^0-9]', '', data[2]))
    else:
        print "Error Connecting to Server"
    return returning_data


# 3:
def return_specific_message(socket, connection_message, message_num):
    message = ""

    if connection_message:
        socket.send("LIST "+message_num+"\r\n")
        message_data = socket.read(2048).split(" ")
        if(message_data[0]!="ERR"):
            message_length = int(re.sub('[^0-9]', '', message_data[2]))
            socket.send("RETR "+message_num+"\r\n")
            amount_received = 0
            while amount_received < message_length:
                data = socket.recv(50000)
                amount_received += len(data)
                message+=data
            msgDate,msgSubject,msgFrom,msgTo,msgBody,msgBodySm="","","","","",""
            for i in xrange(len(message.split("\r\n"))-1):
                if message.split("\r\n")[i].find("Content-Type: text/html")==0:
                    msgBody="".join(message.split("\r\n")[i+1:])
            for element in message.split("\r\n"):
                if element.find("Date:")==0:
                    msgDate=element.replace("Date: ","")[0:-6]
                elif element.find('Delivery-date:')==0:
                    msgDate=element.replace("Delivery-date: ","")[0:-6]
                if element.find("Subject:")==0:
                    msgSubject = element.replace("Subject: ","")
                if element.find("From:")==0:
                    msgFrom = element.replace("From: ","")
                if element.find("To:")==0:
                    msgTo = element.replace("To: ","")
                    break
            #msgBody = html2text.html2text(msgBody)
            if(len(msgBody)>= 40):
                msgBodySm = msgBody[:40]
            else:
                msgBodySm = msgBody
            temp_message={"date":msgDate,"subject":msgSubject,"to":msgTo,"from":msgFrom,"body":msgBody,"bodysm":msgBodySm,"msgnum":message_num}
    else:
        print "Error Connecting to Server"
    return temp_message


# 4:
def return_latest_messages(socket,connection_message):
    mailbox_status = return_server_status(socket,connection_message)
    mailbox_size = int(mailbox_status)
    stop_point = mailbox_size - 10
    latest_messages = []
    if(mailbox_size <=10):
        for counter in range(mailbox_size, 0, -1):
            temp_message=return_specific_message(socket, connection_message, str(counter))
            latest_messages.append(temp_message)
    else:
        latest_messages = return_all_messages(socket, connection_message)
    return latest_messages


# 5:
def return_all_messages(socket, connection_message):
    mailbox_status = return_server_status(socket, connection_message)
    mailbox_size = int(mailbox_status)
    all_messages=[]
    for counter in range(mailbox_size,0,-1):
        temp_message=return_specific_message(socket, connection_message, str(counter))
        all_messages.append(temp_message)
    return all_messages


# 6:
def delete_message(socket, connection_message, message_num):
    if connection_message:
        socket.send("DELE "+str(message_num)+"\r\n")
        response = socket.recv(2048)
        socket.send("QUIT \r\n")
        response += "\n" + socket.recv(2048)
    return response
