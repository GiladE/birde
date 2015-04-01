__author__ = 'JontysLaptop'
import socket
import ssl
import base64
#METHODS FOR COMMUNICATING WITH POP SERVER:
# List:    name                       purpose
#       1: connect_to_server       : connect to SMTP server
#       2: send_mail               : sends an email to a specified address


# 1:
def connect_to_server(host, port):
    connection_state=True
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_clientSocket = ssl.wrap_socket(clientSocket)
    ssl_clientSocket.connect((host, port))
    data = ssl_clientSocket.read(2048)
    if data[:3] != '220':
        return '220 reply not received!'
    else:
        return data, ssl_clientSocket


# 2:
def send_mail(host, port, sender,password, receiver, message_text):
    (connection_message, ssl_client_socket) = connect_to_server(host, port)
    if connection_message[:3] == "220":
        ssl_client_socket.send("HELO \r\n")
        data = ssl_client_socket.recv(1048)
        ssl_client_socket.send("AUTH LOGIN \r\n")
        authentication_message =  ssl_client_socket.recv(1048)
        encodedUser = base64.b64encode(sender)
        encodedPassword = base64.b64encode(password)
        ssl_client_socket.send(""+encodedUser+"\r\n")
        final_authentication_message1 = ssl_client_socket.recv(1048)
        ssl_client_socket.send(""+encodedPassword+"\r\n")
        final_authentication_message = ssl_client_socket.recv(1048)
        if final_authentication_message[:3] == '235':
            ssl_client_socket.send("MAIL FROM: "+sender+"\r\n")
            message1 = ssl_client_socket.recv(1048)
            if message1[:3] == '250':
                ssl_client_socket.send("RCPT TO: "+receiver+"\r\n")
                message2 = ssl_client_socket.recv(1048)
                if message2[:3] == '250':
                    ssl_client_socket.send("DATA \r\n")
                    message3 = ssl_client_socket.recv(1048)
                    if message3[:3] == '354':
                        message_text += "\n."
                        ssl_client_socket.send(message_text)
                        message3 = ssl_client_socket.recv(1048)
                        if message3[:3] == '250':
                            ssl_client_socket.send("QUIT")
                            final_message = ssl_client_socket.recv(1048)
                            return final_message
                        else:
                            return message3
                else:
                    return message2
            else:
                return message1
        else:
            return "250 Reply not Received!"
    else:
        return connection_message


message = send_mail('smtp.gmail.com', 465, 'jsidney006@gmail.com',, 'gilad@eventov.com', 'I am testing the smtp client - reply if you get this message please!')
print message
