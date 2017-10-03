import time
import redis
from datetime import datetime
from celery import task
from django.contrib.auth.models import User
from dashboard.models import UserDateUpdates

# google api imports
from oauth2client.client import AccessTokenCredentials
from googleapiclient.discovery import build
import httplib2
from dashboard.GoogleApi import ListMessagesMatchingQuery, GetAttachments
from DocumentReader.saveDocument import xml_handler as xh

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


@task(name="GoogleConnection")
def googleTask(user1, id):
    user = User.objects.get(username=user1)
    searchdate = datetime.now()
    flag = False
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    services = build("gmail", "v1", http=http)
    gquery = "factura has:attachment xml "
    # Aqui hacer con GetAttachments un buffer para escribir el archivo
    try:
        p = UserDateUpdates.objects.get(UserID=user)
    except UserDateUpdates.DoesNotExist:
        p = UserDateUpdates(
            UserID=user,
            DateCreated=searchdate,
            DateUpdated=searchdate)
        p.save()
        print("imprimiento dates %s" % (p))
    else:
        searchdate = p.DateUpdated
        p.DateUpdated = datetime.now()
        flag = True

    print("User date object %s" % searchdate)

    if flag:
        d = datetime.strftime(searchdate, "%Y/%m/%d")
        de = datetime.strftime(datetime.now(), "%Y/%m/%d")
        gquery = "factura xml has:attachment after: %s before: %s" % (d, de)

    listemails = ListMessagesMatchingQuery(
        services, user1, gquery)

    print("User date gquery %s" % gquery)
    for nlist in listemails:
        print('numero de id: %s' % (nlist['id']))
        f_buffer = GetAttachments(services, user1, nlist['id'])
        if f_buffer:
            xh(f_buffer, id)
        f_buffer = None
