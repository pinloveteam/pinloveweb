'''
Created on 2013-9-24

@author: brad
'''
from django.shortcuts import render
class QtsAuthenticationMiddleware(object):   
#     def process_request(self, request):  
#             if request.user.is_authenticated() or request.path == '/account/register/' or request.path == '/account/forgetpwdpage/':  
#                 pass  
#             else:  
#                 return render(request, 'login.html') 