# coding=UTF-8
'''
Created on Jul 21, 2013

@author: jin
'''
#!/usr/bin/env python
#coding:utf-8
from django import template
register = template.Library()
# @register.filter(name='convertInt',convertInt)
def convertInt(value):
    try:
        value=int(value)
    except:
        print '类型转换失败！'
        pass
    return value
register.filter('convertInt', convertInt)  
