# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
from apps.task_app.tasks import cal_income_task
'''
调用方式1：
 attribute：
   
    args=( operation)
    operation: cal_income
    example:
     1. python manage.py user cal_income
     
         
'''
class Command(BaseCommand):
    def handle(self, *args, **options):
        if args[0]==u'cal_income':
            cal_income_task()