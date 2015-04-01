__author__ = 'JontyHome'
import poplib


class popServer():
    # host = ''
    # username = ''
    # password = ''
    # port = 0


    def __init__(self, username, password, host, port):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.mailbox = poplib.POP3_SSL(self.host,self.port)
        self.mailbox.user(self.username)
        self.mailbox.pass_(self.password)
        self.mailbox.set_debuglevel(1)

    def close_server(self):
        self.mailbox.quit()

    def get_status(self):
        serverstatus = self.mailbox.stat()
        return serverstatus

    def get_messages(self):
        return self.mailbox.list()

    def display_message(self,index):
        (server_msg, body, octets) = self.mailbox.retr(index)
        self.debug(200, "Server Message:    "   , server_msg)
        self.debug(200, "Number of Octets:    " , octets)
        self.debug(200, "Message body:")
        for line in body:
            print line
