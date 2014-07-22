# -*- coding: utf-8 -*-
'''
Created on 2014年7月22日

@author: jin
参考网站http://192.151.154.154/
'''
from django.utils import simplejson
'''
获取ip
'''   
def get_IP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']
'''
获得位置
'''
def get_location(request):
    import httplib
    httpClient = httplib.HTTPConnection('192.151.154.154', 80, timeout=30)
    httpClient.request('GET', '%s%s'%('/json/',get_IP(request)))
    response = httpClient.getresponse()
    return simplejson.loads(response.read())

'''
获取城市代码
'''
def get_country_code(request):
    return get_location(request).get('country_code',None)