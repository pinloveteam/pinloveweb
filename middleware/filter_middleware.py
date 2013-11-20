'''
Created on Nov 19, 2013

@author: jin
'''
from django.shortcuts import render
class AuthenticationMiddleware(object):   
    def process_request(self, request):  
        if not (request.path == '/account/auth/' or request.path == '/'): 
            arg={}
            if request.user.is_authenticated():
                return None  
            else:
                return render(request,'login.html',arg)
        else:
            return None 