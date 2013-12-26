# coding: utf-8 
import os, sys
import datetime
import re
import logging
from pinloveweb.settings import PATH



#Calculate the path based on the location of the WSGI script.

# sys.path.append(r'/home/pinloveteam/webapps/pinlove/pinloveweb')
# 
# os.environ['DJANGO_SETTINGS_MODULE'] = 'pinloveweb.settings'
# 
# os.environ['PYTHON_EGG_CACHE'] = '/tmp'
# 
# 
# import django.core.handlers.wsgi
# 
# 
# application = django.core.handlers.wsgi.WSGIHandler()
# 
# print  sys.stderr, sys.path
# mobilePhone_re=re.compile(r'^1[3|4|5|8][0-9]\d{4,8}$')
# match= mobilePhone_re.match('15558188991')
# print  match.group()

# a=eval('u'+'\u4e95\u5188\u5c71\u5b66\u9662')
# s = '\u56c3\u67e4' 
# i=u'背'
# text = i.decode('GB2312')
# print text
# logger = logging.getLogger('django.db.backends')
# try:
#         from apps.user_app.models import Friend
#         Friend.objects.filter(friend=1)
#     
# except:
#         print '========================='
#         logger.warn("test error")
#         logging.exception('Got exception on main handler')
# from celery.decorators import task
# @task
# def add(x,y):
#     return x+y
# if __name__ =='__main__':
#     result=add.delay(8,8)
#     result.wait()
# =======
# logger = logging.getLogger('django.db.backends')
# try:
#         from apps.user_app.models import Friend
#         Friend.objects.filter(friend=1)
#     
# except:
#         print '========================='
#         logger.warn("test error")
#         logging.exception('Got exception on main handler')
# >>>>>>> Stashed changes 1386963224.48

list=[1,2,3,4]
a=[1,2]
print [x for x in list if x not in a]