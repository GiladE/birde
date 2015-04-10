import socket
import ssl
import base64
#METHODS FOR COMMUNICATING WITH POP SERVER:
# List:    name                       purpose
#       1: connect_to_server       : connect to SMTP server
#       2: send_mail               : sends an email to a specified address


# 1:
def connect_to_server(host, port, username, password):
    connection_state = True
    data = []
    encrypted_username = base64.b64encode(username)
    encrypted_password = base64.b64encode(password)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_clientSocket = ssl.wrap_socket(clientSocket)
    ssl_clientSocket.connect((host, port))
    data.append(ssl_clientSocket.read(2048))
    if data[0][:3] != '220':
        data.append('220 reply not received!')
        connection_state = false
    else:
        ssl_clientSocket.send('ehlo \r\n')
        data.append(ssl_clientSocket.recv(50000))
        if data[1][:3] == '250':
            ssl_clientSocket.send('AUTH LOGIN \r\n')
            data.append(ssl_clientSocket.recv(2048))
            ssl_clientSocket.send(""+encrypted_username+"\r\n")
            data.append(ssl_clientSocket.recv(2048))
            ssl_clientSocket.send(""+encrypted_password+"\r\n")
            data.append(ssl_clientSocket.recv(2048))

        else:
            data.append("Problem requesting authorisation")
            connection_state = false
    return connection_state, data, ssl_clientSocket


# 2:
def send_mail(host, port, username, password, recipiant, message_subject, message_body):
    (state_of_connection, connection_data, ssl_client_socket) = connect_to_server(host, port, username, password)
    final_message = ""
    server_communications = connection_data
    if state_of_connection:
        ssl_client_socket.send("MAIL FROM: <"+username+">\r\n")
        temp_data = ssl_client_socket.recv(2048)
        if temp_data[:3] == '250':
            server_communications.append(temp_data)
            temp_data = ""
            ssl_client_socket.send("RCPT TO: <"+recipiant+">\r\n")
            temp_data = ssl_client_socket.recv(2048)
            if temp_data[:3] == '250':
                server_communications.append(temp_data)
                temp_data = ""
                ssl_client_socket.send("DATA \r\n")
                temp_data = ssl_client_socket.recv(2048)
                if temp_data[:3] == '354':
                    server_communications.append(temp_data)
                    temp_data = ""
                    final_message = "Subject: "+message_subject+"\nFrom: <"+username+">\nTo: <"+recipiant+">\nContent-Type: text/html; charset=UTF-8\n<div dir='ltr'>"+message_body.replace("\n","<br/>")+"</div>\n.\r\n"
                    ssl_client_socket.send(final_message)
                    temp_data = ssl_client_socket.recv(2048)
                    if temp_data[:3] == '250':
                        server_communications.append(temp_data)
                        temp_data = ""
                        ssl_client_socket.send("quit \r\n")
                        #temp_data = ssl_client_socket.recv(2048)
                        #server_communications.append(temp_data)
                    else:
                        server_communications.append(temp_data)
                        temp_data = ""
            else:
                server_communications.append(temp_data)
                temp_data = ""
        else:
            server_communications.append(temp_data)

    else:
        server_communications.append("Error connecting to SMTP.")
    return server_communications

