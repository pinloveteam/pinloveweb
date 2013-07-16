# -*- coding: utf-8 -*-

# from django.http import HttpResponse 

from django.shortcuts import render 
from django.http import HttpResponseRedirect 
from django.contrib import auth 
from django.core.context_processors import csrf 

from django.contrib.auth.models import User 

from django.core.mail import send_mail

from forms import RegistrationForm 
from pinloveweb import settings

def login(request) :
       
    unicode_s = u'欢迎来到拼爱网'
    
    if request.user.is_authenticated() :
        return HttpResponseRedirect('/account/loggedin/')
    else : 
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 

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
    
    return render(request, 'loggedin.html', {'full_name': request.user.username,'set':settings.STATIC_ROOT})
    
def invalid_login(request) : 
    
    return render(request, 'invalid_login.html')
    
def logout(request) : 
    
    auth.logout(request)
    return HttpResponseRedirect("/account/loggedout/")
    
def loggedout(request) : 
    
    return render(request, 'loggedout.html')
    
def register_user(request) : 
    
    args = {}
    args.update(csrf(request))
    
    if request.method == 'POST' : 
        userForm = RegistrationForm(request.POST) 
        if userForm.is_valid() :
            userForm.save()
            
            username = userForm.cleaned_data['username']
            # password = user_form.clean_password2()
            # user = authenticate(username=username, password=password)
            user = User.objects.get(username=username)
            user.is_active = False 
            
            # we need to generate a random number as the verification key 
            
            # user needs email verification 
            domain_name = u'http://127.0.0.1:8000/account/verification/'
            email_verification_link = domain_name + username + '/'
            
            email_message = u"请您点击下面这个链接完成注册："
            email_message += email_verification_link
            send_mail(u'拼爱网注册电子邮件地址验证', email_message, 'lospadres663@gmail.com',['eqyzou@gmail.com']) 
            
            # login(request, user)

            
            return HttpResponseRedirect('/account/register_verify/')
            # return HttpResponseRedirect('/account/register_success/') 
        else : 
            args['user_form'] = userForm
    else : 
        args['user_form']= RegistrationForm() 
    
    return render(request, 'register.html', args)
    
def register_success(request) : 
    return render(request, 'register_success.html')
    
def register_verify(request) : 
    return render(request, 'register_email_verification.html')
    

    
 
                          
                          
        
        