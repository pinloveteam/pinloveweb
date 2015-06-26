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
        redirectUrl=''
        passList=['/android_download/','/user/reset_password/','/account/forget_password/','/account/auth/','/account/register/','/','/game/jigsaw/','/game/pintu_for_facebook/','/pay_app/icon/','/pay_app/exchange_game_count/','/game/request_life/',
                  '/game/confirm_request_life/(.+)/','/account/check_register/','/mobile/register/','/mobile/auth/','/mobile/','/mobile/forget_password/','/mobile/logout/','/test/','/weixin/download/']
        facebookPattern = re.compile(r'^/game/|/pay/|/alipay/')
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
                if re.compile(r'^/mobile').match(request.path) is None:
                    redirectUrl='/'
                else:
                    redirectUrl='/mobile/'
                if request.path in ['/account/loggedout/','/account/invalid/','/mobile/logout']:
                    return HttpResponseRedirect(redirectUrl)
                else:
                    return HttpResponseRedirect('%s%s%s'%(redirectUrl,'?next=',request.path))
        else:
            return None

