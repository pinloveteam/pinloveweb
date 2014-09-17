# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import simplejson
from django.contrib.auth.models import User
'''
调用方式1：
 attribute：
   
    args=( operation,userId)
    example:
     1. python manage.py user del 1
     
         
'''
class Command(BaseCommand):
    def handle(self, *args, **options):
#         self.stdout.write(simplejson.dumps(options))
#         self.stdout.write(simplejson.dumps(args))
        if args[0]=='del':
          User.objects.filter(id=args[1]).delete()
        self.stdout.write('success!')