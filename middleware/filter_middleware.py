'''
Created on Nov 19, 2013

@author: jin
'''
from django.http.response import HttpResponseRedirect, HttpResponse
import re
import simplejson
class AuthenticationMiddleware(object):   
    def process_request(self, request):  
        passList=['/account/forgetpwdpage/','/account/auth/','/account/register/','/','/game/pintu_for_facebook_url/','/game/pintu_for_facebook/']
        pattern = re.compile(r'^/admin/|/third_party_login/|/login/|/complete/')
        match = pattern.match(request.path)
        if match!=None:
            return None
        if not ((request.path in passList )or (request.path.find('.')!=-1)): 
            if request.user.is_authenticated():
                return None  
            else:
                if request.REQUEST.get('ajax',False):
                    json=simplejson.dumps({'login':'invalid','redirectURL':'/?next=request.path'})
                    return HttpResponse(json)
                if request.path in ['/account/loggedout/','/account/invalid/']:
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/?next='+request.path)
        else:
            return None
