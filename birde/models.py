from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser

class Connection (models.Model):
    user = models.OneToOneField(User)
    popHost = models.CharField(max_length=200,default=None)
    popPort = models.IntegerField(default=None)
    popUser = models.CharField(max_length=200,default=None)
    popPass = models.CharField(max_length=200,default=None)
    smtpHost = models.CharField(max_length=200,default=None)
    smtpPort = models.IntegerField(default=None)
    smtpUser = models.CharField(max_length=200,default=None)
    smtpPass = models.CharField(max_length=200,default=None)

class Chat (models.Model):
    user = models.OneToOneField(User)
    online = models.BooleanField(default=False)

class Message(models.Model):
    owner = models.ForeignKey(User)
    sender = models.CharField(max_length=200)
    recipient = models.CharField(max_length=200)
    dateSent = models.DateTimeField('date sent')
    subject = models.CharField(max_length=500)
    body = models.CharField(max_length=50000)
    type = models.BooleanField(default=False)
