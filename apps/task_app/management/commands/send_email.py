# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
from apps.user_app.models import UserProfile
import logging
from apps.task_app.email import send_notify_email, send_message_email
from apps.task_app.models import TaskRecode
logger=logging.getLogger(__name__)
'''
调用方式1：
 attribute：
   
    args=( operation)python manage.py 
    operation: python manage.py  send_email type [userId,[userId,[....]]]
    example:
     1. python manage.py send_email
     
      1. python manage.py send_email 1,2,3,4
         
'''
class Command(BaseCommand):
    def handle(self, *args, **options):
      try:
        message=''
        flag=True
        temp=''
        if args[0]=='recommend':
            if len(args)==1:
                send_notify_email()
            else:
                temp='%s%s'%('用户ids：',args[1])
                userIdList=[ int(attr) for attr in args[1].split(',')]
                send_notify_email(userIdList=userIdList)
            message='发送推荐邮件成功!'
        elif args[0]=='message':
            if len(args)==1:
                send_message_email()
            else:
                self.stdout.write('111')
                temp='%s%s'%('用户ids：',args[1])
                userIdList=[ int(attr) for attr in args[1].split(',')]
                send_message_email(userIdList=userIdList)
            message='发送推荐邮件成功!'
        else:
            message='参数错误!'
            flag=False
        self.stdout.write(message)
        if flag:
            #添加任务记录
            TaskRecode(content='%s%s'%('发送推荐邮件 ',temp),result='success').save()
      except Exception as e:
          #添加任务记录
          TaskRecode(content='%s%s'%('发送推荐邮件 ',temp),data=e.message).save()
          self.stdout.write(e.message)
      finally:
          self.stdout.write('end')
          