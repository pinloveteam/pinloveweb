# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2013

@author: jin
'''
import string
import random
'''
生成长度固定的字符串
'''
def random_str(randomlength=32):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])
