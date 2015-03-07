# -*- coding: utf-8 -*-
'''
Created on 2015年3月7日

@author: jin
'''
import re
import urlparse
'''
判断客户端返回回调连接
'''
def judge_client(request,return_url):
    if  re.match('^/mobile',request.path)  is not None:
        return_url='%s%s'%(return_url,'?next_url=/mobile/loggedin/')
    else:
        return_url='%s%s'%(return_url,'?next_url=/account/loggedin/')
    return return_url

'''
从回调连接中获取跳转链接连接
'''
def get_next_url_by_callback_url(url):
    parsed=urlparse.urlparse(url)
    next_url=urlparse.parse_qs(parsed.query).get('next_url')  
    return next_url
    
