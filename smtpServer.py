__author__ = 'JontyHome'
import smtplib


class smtpServer(object):
    host = ''
    port = 0
    smtp_server
    username = ''
    password = ''

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.smtp_server = smtplib.SMTP(self.host,self.port)
        self.smtp_server.starttls()
        self.smtp_server.login(self.username,self.password)

    def close_server(self):
        self.smtp_server.quit()

    def identify_server(self):
        self.smtp_server.helo(self.host)

    def send_mail(self, receiver, sender, message):
        self.smtp_server.sendmail(sender,receiver,message)
