# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
from apps.user_app.models import UserProfile
import logging
loger=logging.getLogger(__name__)
'''
调用方式1：
 attribute：
   
    args=( operation)python manage.py 
    operation: task ,test_education
    example:
     1. python manage.py user task
     
         
'''
class Command(BaseCommand):
    def handle(self, *args, **options):
      try:
        if args[0]==u'task':
            from apps.task_app.tasks import task_run
            task_run()
        elif args[0]==u'test_education':
            userProfile=UserProfile.objects.get(user_id=args[1])
            from apps.task_app.tasks import cal_education_task
            result=cal_education_task(userProfile.user_id,userProfile.gender,userProfile.education,userProfile.educationSchool,userProfile.educationSchool_2,True)
            self.stdout.write(result)
      except Exception as e:
          self.stdout.write(e.message)
      finally:
          self.stdout.write('sdf')
             