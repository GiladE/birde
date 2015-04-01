__author__ = 'JontyHome'
import popServer


print("POP3 Server Configuration")
host = raw_input("Enter the Server Address:")
port = int(raw_input("Enter the correct Port:"))
user = raw_input("Enter your Username:")
password = raw_input("Enter your Password:")

myPopServer = popServer.popServer(user, password, host, port)

myStatus = myPopServer.get_status()
print myStatus

myMail = myPopServer.get_messages()
print myMail

myPopServer.display_message(2)
