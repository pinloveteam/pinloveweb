# -*- coding: utf-8 -*-
'''
Created on Nov 19, 2013

@author: jin
'''
from django.http.response import HttpResponseRedirect, HttpResponse
import logging
logger=logging.getLogger(__name__)
import re
from django.utils import simplejson
#登录拦截中间件
class AuthenticationMiddleware(object):   
    def process_request(self, request):  
        passList=['/user/reset_password/','/account/forget_password/','/account/auth/','/account/register/','/','/game/jigsaw/','/game/pintu_for_facebook/','/pay_app/icon/','/pay_app/exchange_game_count/','/game/request_life/','/game/confirm_request_life/(.+)/','/account/check_register/']
        facebookPattern = re.compile(r'^/game/|/pay/|/weixin/|/alipay/')
        facebookMatch = facebookPattern.match(request.path)
        pattern = re.compile(r'^/admin/|/third_party_login/|/login/|/complete/')
        match = pattern.match(request.path)
        if request.path!='/pay/pay_paypal/' and( match!=None or facebookMatch!=None):
            return None
        if not ((request.path in passList )or (request.path.find('.')!=-1)): 
            if request.user.is_authenticated():
                return None  
            else:
                if request.is_ajax():
                    json=simplejson.dumps({'login':'invalid','redirectURL':'/?next='+request.path})
                    return HttpResponse(json)
                if request.path in ['/account/loggedout/','/account/invalid/']:
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/?next='+request.path)
        else:
            return None