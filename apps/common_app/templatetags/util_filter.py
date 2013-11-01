# coding=UTF-8
'''
Created on Jul 21, 2013

@author: jin
'''
from django import template
register = template.Library()
@register.filter
def mod(value,var):
    try:
        value=int(value)
        var=int(var)
    except:
        pass
    value=value%var
    return value
# register.filter('MOD', MOD)  

'''
test
'''
if __name__=='__main__':
    print mod(10)
    