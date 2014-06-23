# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import simplejson
'''
调用方式1：
 attribute：
   
    args=( cache,key1,userId,key2)
    example:
     1. python manage.py util cache HAS_RECOMMEND
     2.python manage.py util cache HAS_RECOMMEND 5
     3.python manage.py util cache HAS_RECOMMEND 5 userExpect
         
'''
class Command(BaseCommand):
    def handle(self, *args, **options):
#         self.stdout.write(simplejson.dumps(options))
#         self.stdout.write(simplejson.dumps(args))
        if args[0]=='cache':
            if len(args)==2:
                self.stdout.write(simplejson.dumps(cache.get(args[1],'')))
            elif len(args)==3:
                cahceList=cache.get(args[1],'')
                self.stdout.write(simplejson.dumps(cahceList.get(int(args[2]))))
            else:
                cahceList=cache.get(args[1],'')
                dict=cahceList.get(int(args[2]))
                self.stdout.write(simplejson.dumps(dict))
                self.stdout.write(u'%s%s%s'%(args[3],':',dict.get(args[3])))
        self.stdout.write('success!')