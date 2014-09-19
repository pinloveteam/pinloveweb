# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
'''
调用方式1：
 attribute：
   
    args=( operation)
    operation: task
    example:
     1. python manage.py user task
     
         
'''
class Command(BaseCommand):
    def handle(self, *args, **options):
        if args[0]==u'task':
            from apps.task_app.tasks import task_run
            task_run()