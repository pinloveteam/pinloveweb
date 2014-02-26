# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2013

@author: jin
'''
import string
import random
import urllib 
from json import loads, JSONEncoder

from django.core.serializers import serialize
from django.db.models.query import QuerySet
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
    
class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        return JSONEncoder.default(self,obj)
'''
转换类成dict
instance[class]:类
fields:属性
'''   
def model_to_dict(instance,fields=None):
    list=[]
    for object in instance:
        args={}
        for field in fields:
            args[field]=getattr(object,field)
        list.append(args)
    return list

