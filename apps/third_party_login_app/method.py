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
    if  request.REQUEST.get('channel',None)  == 'mobile':
        return_url='%s%s'%(return_url,'?next_url=/mobile/loggedin/')
    else:
        return_url='%s%s'%(return_url,'?next_url=/account/loggedin/')
    return return_url

    
