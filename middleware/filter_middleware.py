'''
Created on Nov 19, 2013

@author: jin
'''
from django.http.response import HttpResponseRedirect
import re
class AuthenticationMiddleware(object):   
    def process_request(self, request):  
        passList=['/account/forgetpwdpage/','/account/auth/','/account/register/','/',]
        pattern = re.compile(r'^/admin/|/third_party_login/|/login/|/complete/')
        match = pattern.match(request.path)
        if match!=None:
            return None
        if not ((request.path in passList )or (request.path.find('.')!=-1)): 
            if request.user.is_authenticated():
                return None  
            else:
                if request.path=='/account/loggedout/':
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/?redirectURL='+request.path)
        else:
            return None
