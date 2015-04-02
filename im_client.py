__author__ = 'JontyHome'
import socket

host = raw_input("Enter the IP Address of the host you wish to chat with:")
port = 50007
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))
chat_active = True
while chat_active:
    send_message = raw_input("Reply:")
    if send_message == 'END':
        client_socket.send(send_message)
        client_socket.close()
        chat_active = False
        break
    else:
        client_socket.send(send_message)
    data = client_socket.recv(2048)
    print 'Received Data: ', repr(data)
    if data == 'END':
        client_socket.send("END")
        client_socket.close()
        chat_active = False
        break
    send_message = ""
client_socket.close()
