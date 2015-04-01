from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    owner = models.ForeignKey(User)
    sender = models.CharField(max_length=200)
    recipient = models.CharField(max_length=200)
    dateSent = models.DateTimeField('date sent')
    subject = models.CharField(max_length=500)
    body = models.CharField(max_length=50000)
    type = models.BooleanField(default=False)
