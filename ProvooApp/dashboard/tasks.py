import time
import redis
from celery import task
from django.contrib.auth.models import User

# google api imports
from oauth2client.client import AccessTokenCredentials
from googleapiclient.discovery import build
import httplib2
from dashboard.GoogleApi import ListMessagesMatchingQuery, GetAttachments
from DocumentReader.saveDocument import xml_handler as xh

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


@task(name="Sum")
def addt(a, b):
    return a + b


@task(name="GoogleConnection")
def googleTask(user, id):
    user = User.objects.get(username=user)
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    services = build("gmail", "v1", http=http)
    # Aqui hacer con GetAttachments un buffer para escribir el archivo
    listemails = ListMessagesMatchingQuery(
        services, user, "factura has:attachment xml ")
    for nlist in listemails:
        print('numero de id: %s' % (nlist['id']))
        f_buffer = GetAttachments(services, user, nlist['id'])
        if f_buffer:
            xh(f_buffer, id)
        f_buffer = None
