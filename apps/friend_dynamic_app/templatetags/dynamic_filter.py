# coding=UTF-8
'''
Created on Jul 21, 2013

@author: jin
'''
from django import template
register = template.Library()
@register.filter
def get_list_number(value,num):
    result=value[num]
    return result
# register.filter('get_list_num', get_list_num)  

'''
test
'''
if __name__=='__main__':
    print get_list_number([True,False,False],1)
    