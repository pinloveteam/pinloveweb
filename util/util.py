# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2013

@author: jin
'''
import string
import random
import urllib 
'''
生成长度固定的字符串
'''
def random_str(randomlength=32):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def download_pic(url,filename):
#     urllib.urlretrieve(url, "00000001.jpg")
    data = urllib.urlopen(url).read() 
    f = file(filename,"wb") 
    f.write(data) 
    f.close() 
