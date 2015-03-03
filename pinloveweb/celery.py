'''
Created on Nov 28, 2013

@author: jin
'''
from __future__ import absolute_import

import os
from celery.app.base import Celery
from pinloveweb import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pinloveweb.settings')

app = Celery('pinloveweb')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))