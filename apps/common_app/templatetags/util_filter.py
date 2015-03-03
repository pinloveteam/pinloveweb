# coding=UTF-8
'''
Created on Jul 21, 2013

@author: jin
'''
from django import template
register = template.Library()
'''
求余
attribute：
      value:本身的值
      var：传入值
'''
@register.filter
def mod(value,var):
    try:
        value=int(value)
        var=int(var)
    except:
        pass
    value=value%var
    return value

'''
大于
attribute：
      value:本身的值
      var：传入值
'''
@register.filter
def greater_than(value,var):
    try:
        value=int(value)
        var=int(var)
    except:
        pass
    if value>var:
        return True
    else:
        return False
    
@register.filter
def initial_choice(form, field_name):
    return dict(form.fields[field_name].choices)[form.initial[field_name]]
'''
test
'''
if __name__=='__main__':
    print mod(10)
    