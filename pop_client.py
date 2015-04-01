__author__ = 'JontysLaptop'
import socket
import ssl
import re

#METHODS FOR COMMUNICATING WITH POP SERVER:
# List:    name                   purpose
#       1: connect_to_server       : connect to POP server and verify user credentials
#       2: return_server_status    : returns the number of messages in the mailbox as well as the size of the mailbox
#       3: return_specific_message : returns a specific message as specified by the user


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
                connection_state=True
    return connection_state, ssl_clientSocket


# 2:
def return_server_status(host, port, username, password):
    returning_data = [2]
    (connection_message, ssl_client_socket) = connect_to_server(host, port, username, password)
    if connection_message:
        ssl_client_socket.send("STATE \r\n")
        data = ssl_client_socket.read(2048).split(" ")
        returning_data[0] = data[1]
        returning_data[2] = re.sub('[^0-9]','',data[2])
        ssl_client_socket.close()
    else:
        print "Error Connecting to Server"
    return returning_data


# 3:
def return_specific_message(host, port, username, password, message_num):
    message = []
    (connection_message, ssl_client_socket) = connect_to_server(host, port, username, password)
    if connection_message:
        ssl_client_socket.send("LIST "+message_num+"\r\n")
        message_data = ssl_client_socket.read(2048).split(" ")
        message_length = int(re.sub('[^0-9]', '', message_data[2]))
        ssl_client_socket.send("RETR "+message_num+"\r\n")
        amount_received = 0
        while amount_received < message_length:
            data = ssl_client_socket.recv(50000)
            amount_received += len(data)
            message.append(data)
        ssl_client_socket.close()
    else:
        print "Error Connecting to Server"
    return message
