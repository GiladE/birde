__author__ = 'JontyHomeLol'
import socket
import ssl
import re

#METHODS FOR COMMUNICATING WITH POP SERVER:
# List:    name                   purpose
#       1: connect_to_server       : connect to POP server and verify user credentials.
#       2: return_server_status    : returns the number of messages in the mailbox as well as the size of the mailbox.
#       3: return_specific_message : returns a specific message as specified by the user.
#       4: return_latest_messages  : returns the latest 20 messages on the mailbox.

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
    message = []
    
    if connection_message:
        socket.send("LIST "+message_num+"\r\n")
        message_data = socket.read(2048).split(" ")
        message_length = int(re.sub('[^0-9]', '', message_data[2]))
        socket.send("RETR "+message_num+"\r\n")
        amount_received = 0
        while amount_received < message_length:
            data = socket.recv(50000)
            amount_received += len(data)
            message.append(data)
        
    else:
        print "Error Connecting to Server"
    return message


# 4:
def return_latest_messages(socket,connection_message):
    mailbox_status = return_server_status(socket,connection_message)
    mailbox_size = int(mailbox_status)
    stop_point = mailbox_size - 5
    latest_messages = []
    for counter in range(mailbox_size, stop_point, -1):
        raw_message = return_specific_message(socket, connection_message, str(counter))
        msgDate,msgSubject,msgFrom,msgTo,msgBody="","","","",""
        for i in xrange(len(raw_message[1].split("\r\n"))-1):
            if raw_message[1].split("\r\n")[i].find("Content-Type: text/html")==0:
                msgBody="".join(raw_message[1].split("\r\n")[i+1:])
        for element in raw_message[1].split("\r\n"):
            if element[0:4]=="Date:":
                msgDate=element.replace("Date: ","")[0:-6]
            if element[0:7]=="Subject:":
                msgSubject = element.replace("Subject: ","")
            if element[0:4]=="From:":
                msgFrom = element.replace("From: ","")
            if element[0:2]=="To:":
                msgTo = element.replace("To: ","")
              #  break

        temp_message={"date":msgDate,"subject":msgSubject,"to":msgTo,"from":msgFrom,"body":msgBody}
        latest_messages.append(temp_message)
    return latest_messages


# For Testing Purpose:s
myhost ="pop.gmail.com"
myusername ="gilad@eventov.com"
myport =995
mypassword ="vepkwhhtypmsmivy"
my_connection_message, my_socket = connect_to_server(myhost, myport, myusername, mypassword)
server_info = return_server_status(my_socket, my_connection_message)
print server_info
print "New Messages:"
print "_____________"
newest_messages = return_latest_messages(my_socket,my_connection_message)
print newest_messages
for i in newest_messages:
    print i
#for i in newest_messages:
#    print repr(i)
# newestmessage=return_specific_message(my_socket, my_connection_message,"1")
# print newestmessage[1].split("\r\n")
my_socket.close()
