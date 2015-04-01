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
    if data[:3] != '220':
        return '220 reply not received!'
    else:
        return data

message = connect_to_server('smtp.gmail.com', 465, 'jsidney006@gmail.com', 'drzkdwvqkxrhzsfx')
print message
