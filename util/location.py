# -*- coding: utf-8 -*-
'''
Created on 2014年7月22日

@author: jin
参考网站http://192.151.154.154/
'''
from django.utils import simplejson
import logging
logger=logging.getLogger("django")
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
   try:
    import urllib2
    url='%s%s'%('http://freegeoip.net/json/',get_IP(request))
    req = urllib2.Request(url)
    response = urllib2.urlopen(req,timeout = 5)
    return simplejson.loads(response.read())
   except Exception, e:  
        logger.error('访问freegeoip超时')
        return {}  


'''
获取城市代码
'''
def get_country_code(request):
    return get_location(request).get('country_code',None)