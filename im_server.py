__author__ = 'JontyHome'
import socket
import ssl

host = raw_input("Enter the IP Address of your PC:")
port = 50007

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host,port))
server_socket.listen(1)
conn, addr = server_socket.accept()

chat_active = True
print 'Connected to:', addr
while chat_active:
    received_message = conn.recv(2048)
    print repr(received_message)
    if received_message == 'END':
        print "Client disconnected."
        chat_active = False
        conn.close()
        break
    reply = raw_input("Reply:")
    conn.send(reply)
    reply = ""
conn.close()
