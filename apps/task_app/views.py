# -*- coding: utf-8 -*-
'''
Created on Nov 28, 2013

@author: jin
'''
from django.http import HttpResponse
from apps.task_app import tasks
 
# def test_celery(request):
#     result = tasks.add.delay(1,3)
#     return HttpResponse(result)
def test_celery(request): 
    from pinloveweb.settings import DEFAULT_FROM_EMAIL
    emails=(('0','i asdasd',DEFAULT_FROM_EMAIL, ['jin521436@163.com']),)
    for i in range(1,2):
        emails+=((str(i),'i asdasd',DEFAULT_FROM_EMAIL, ['jin521436@163.com']),)
    from django.core import mail
    results = mail.send_mass_mail(emails)
    return HttpResponse("发送成功")
