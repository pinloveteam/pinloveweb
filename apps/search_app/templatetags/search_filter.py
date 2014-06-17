# coding=UTF-8
'''
Created on Jul 21, 2013

@author: jin
'''
from django import template
register = template.Library()
#!/usr/bin/env python
#coding:utf-8
'''
求余
attribute：
      value:本身的值
      var：传入值
'''
@register.filter
def sunSign(value,var):
    try:
        value=int(value)
        var=int(var)
    except:
        pass
    if value==0:
        value=2
    else:
        value=value%var
    return value
   


