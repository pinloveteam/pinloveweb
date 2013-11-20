'''
Created on Nov 19, 2013

@author: jin
'''
from django.http.response import HttpResponseRedirect
class AuthenticationMiddleware(object):   
    def process_request(self, request):  
        if not (request.path == '/account/auth/' or request.path == '/' or request.path.find('.')!=-1): 
            if request.user.is_authenticated():
                return None  
            else:
                return HttpResponseRedirect('/account/login/')
        else:
            return None
