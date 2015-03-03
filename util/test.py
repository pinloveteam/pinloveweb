# -*- coding: utf-8 -*-
'''
Created on Sep 1, 2013

@author: jin
'''
from util.common_util import random_str
import time
print random_str(randomlength=2)
print time.strftime('%Y%m%d',time.localtime(time.time()))
s="asdfsdfsfs.png"
print(s[s.find('.'):])
