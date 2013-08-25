# coding=UTF-8
'''
Created on Jul 21, 2013

@author: jin
'''
#!/usr/bin/env python
#coding:utf-8
from django import template
register = template.Library()
i=0
@register.filter(name='qwer')
def qwer(value):
    global i
    print i
    if i<len(value):
        value = value[i]
        i=i+1
        return str(value)
    else:
        return "0"
   


