# -*- coding: utf-8 -*-

# from django.http import HttpResponse 

from django.shortcuts import render 
from django.http import HttpResponseRedirect 
from django.contrib import auth 
from django.core.context_processors import csrf 

def login(request) :
       
    unicode_s = u'欢迎来到拼爱网'
    
    if request.user.is_authenticated() :
        return HttpResponseRedirect('/account/loggedin/')
    else : 
        c = {}
        c.update(csrf(request))
        return render(request, 'login.html', c) 

def auth_view(request) : 
    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    
    if user is not None and user.is_active : 
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page 
        return HttpResponseRedirect('/account/loggedin/')
    else : 
        # Show an error page 
        return HttpResponseRedirect('/account/invalid/')
        
def loggedin(request) : 
    
    return render(request, 'loggedin.html', {'full_name': request.user.username})
    

def invalid_login(request) : 
    
    return render(request, 'invalid_login.html')
    
def logout(request) : 
    
    auth.logout(request)
    return HttpResponseRedirect("/account/loggedout/")
    
def loggedout(request) : 
    
    return render(request, 'loggedout.html')

def register(request) : 
    
    return render(request, 'register.html')
    
 
                          
                          
        
        