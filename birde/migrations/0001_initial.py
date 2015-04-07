# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('popHost', models.CharField(default=None, max_length=200)),
                ('popPort', models.IntegerField(default=None)),
                ('popUser', models.CharField(default=None, max_length=200)),
                ('popPass', models.CharField(default=None, max_length=200)),
                ('smtpHost', models.CharField(default=None, max_length=200)),
                ('smtpPort', models.IntegerField(default=None)),
                ('smtpUser', models.CharField(default=None, max_length=200)),
                ('smtpPass', models.CharField(default=None, max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.CharField(max_length=200)),
                ('recipient', models.CharField(max_length=200)),
                ('dateSent', models.DateTimeField(verbose_name=b'date sent')),
                ('subject', models.CharField(max_length=500)),
                ('body', models.CharField(max_length=50000)),
                ('type', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
