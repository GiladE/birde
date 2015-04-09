__author__ = 'JontyHome'
import socket
import sys
import thread

HOST = '' # all availabe interfaces
PORT = 9999 # arbitrary non privileged port

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
    sys.exit(0)

print("[-] Socket Created")

# bind socket
try:
    s.bind((HOST, PORT))
    print("[-] Socket Bound to port " + str(PORT))
except socket.error, msg:
    print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
    sys.exit()

s.listen(10)
print("Listening...")

# The code below is what you're looking for ############

def client_thread(conn):
    conn.send("Welcome to the Server. Type messages and press enter to send.\n")

    while True:
        data = conn.recv(1024)
        # if not data:
        #     break
        # else:
        print (addr[0]+":"+str(addr[1]) + " Sent: " + data)
        receive_address = data.split(" ",1)[0]
        receive_address = receive_address.strip("[]")
        (add_1,add_2)= receive_address.split(":")
        send_to = (add_1, int(add_2))

        # print send_to
        reply = "FROM: " +addr[0]+":"+str(addr[1]) +": \n" + data[1]
        conn.sendto(reply, send_to)
    conn.close()

while True:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

    thread.start_new_thread(client_thread, (conn,))

s.close()
