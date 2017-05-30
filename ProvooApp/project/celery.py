
from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery('project')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    BROKER_URL='redis://redis:6379/0',
    CELERY_RESULT_BACKEND='redis://redis:6379/0',
)
