# -*- coding: utf-8 -*-
'''
Created on Nov 29, 2013

@author: jin
'''
from django.core.mail.backends.base import BaseEmailBackend
from apps.task_app.tasks import send_email



class CeleryEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super(CeleryEmailBackend, self).__init__(fail_silently)
        self.init_kwargs = kwargs

    def send_messages(self, email_messages, **kwargs):
        results = []
        kwargs['_backend_init_kwargs'] = self.init_kwargs
        for msg in email_messages:
            results.append(send_email.delay(msg, **kwargs))
        return results