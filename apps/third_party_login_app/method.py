# -*- coding: utf-8 -*-
'''
Created on 2015年3月7日

@author: jin
'''
import re
import urlparse
from django.contrib.auth import get_backends
'''
判断客户端返回回调连接
'''
def judge_client(request,return_url):
    if  request.REQUEST.get('channel',None)  == 'mobile':
        return_url='%s%s'%(return_url,'?next_url=/mobile/loggedin/')
    else:
        return_url='%s%s'%(return_url,'?next_url=/account/loggedin/')
    return return_url

    
def authenticate_three_party_login(**credentials):
    """
    If the given credentials are valid, return a User object.
    第三方登录
    """
    for backend in get_backends():
        try:
            user = backend.authenticate_three_party_login(**credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue
        if user is None:
            continue
        # Annotate the user object with the path of the backend.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return user