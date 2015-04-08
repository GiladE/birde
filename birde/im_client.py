__author__ = 'JontyHome'
import socket

HOST = '192.168.0.10'    # The remote host
PORT = 9999             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
chat_partner = raw_input("Enter the IP of the client you wish to chat with")
while True:
    send_data = raw_input("Enter a Message:")
    s.sendall("["+chat_partner+"] "+send_data)
s.close()
