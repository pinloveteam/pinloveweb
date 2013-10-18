# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2013

@author: jin
'''
from django.shortcuts import render
from apps.user_app.models import UserVerification, UserProfile, Verification,\
    UserContactLink
from django.core.mail import send_mail
import string
import random
from django.core.exceptions import ValidationError
from apps.verification_app.forms import IDCardValidForm, IncomeValidForm,\
    EducationValidForm
from django.conf import settings

def verif_list(request):
    arg={}
    if request.user.is_authenticated():
      try:
        userVerification=UserVerification.objects.get(user=request.user)
      except UserVerification.DoesNotExist:
          userVerification=UserVerification()
          userVerification.user=request.user
          userVerification.save()
      avatarStatus=UserProfile.objects.get(user=request.user).get_avatar_name_status_display()
     
      arg['avatarStatus']=avatarStatus
      arg['emailValid']=userVerification.get_emailValid_display()
      arg['mobileNumberValid']=userVerification.get_mobileNumberValid_display()
      arg['incomeValid']=userVerification.get_incomeValid_display()
      arg['educationValid']=userVerification.get_educationValid_display()
      arg['IDCardValid']=userVerification.get_IDCardValid_display()
      return render(request,'list.html',arg)
    else:
      return render(request,'login.html',arg)  
  
def emailvalid(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=='POST':
            email=request.POST.get('email')
            user=request.user
            if email.strip()!='':
                if email==user.email:
                     sendmail(user)
                else:
                     from django.contrib.auth.models import User
                     if User.objects.filter(email=email).exists():
                         arg['error_message']=r'该邮箱已经被注册'
                         arg['email']=email
#                          raise ValidationError(r"该邮箱已经被注册!")  
                         return render(request,'emailvalid.html',arg)
                     user.email=email
                     sendmail(user)
                     user.save()
            return render(request,'success.html',arg)
        else:
            return render(request,'emailvalid.html',arg)
    else:
      return render(request,'login.html',arg) 
def sendmail(user):
     user_code = random_str()
     if Verification.objects.filter(username=user.username).exists():
        Verification.objects.filter(username=user.username).update(verification_code=user_code)
     else:
        verification = Verification()
        verification.username = user.username
        verification.verification_code = user_code
        verification.save()
     # user needs email verification 
     domain_name = u'http://127.0.0.1:8000/verification/emailValidConfirm/'
     email_verification_link = domain_name + '?username=' + user.username + '&' + 'user_code=' + user_code
     email_message = u"请您点击下面这个链接完成注册："
     email_message += email_verification_link
     try :
       send_mail(u'拼爱网注册电子邮件地址验证', email_message,'pinloveteam@pinpinlove.com',[user.email]) 
     except:
        print u'邮件发送失败'
        pass
def random_str(randomlength=32):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def emailvalid_confirm(request) : 
    username = request.REQUEST.get('username','')
#     user_code = request.REQUEST.get('user_code','')
    from django.contrib.auth.models import User
    user = User.objects.get(username=username)
#     verification = Verification.objects.get(username=username)
    from apps.user_app.views import isIdAuthen
    if isIdAuthen(request):
        UserVerification.objects.filter(user=user).update(emailValid='2')
#         verification.delete()
        return render(request, 'verfication_success.html')
    else :
        return render(request, 'error.html')
    
'''
 身份验证
'''
def IDcard_valid(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=='POST':
            userContactLink=UserContactLink.objects.get(user=request.user)
            IDcardValidForm=IDCardValidForm(request.POST,request.FILES,instance=userContactLink)
            if IDcardValidForm.is_valid():
                userVerification=UserVerification.objects.get(user=request.user)
                userVerification.IDCardPicture=IDcardValidForm.cleaned_data['IDCardPicture']
                userVerification.IDCardValid=2
                userContactLink=IDcardValidForm.save(commit=False)
                userVerification.save()
                userContactLink.save()
                return render(request,'verfication_success.html',arg)
            else:
                 arg['IDcardValidForm']=IDcardValidForm
                 return render(request,'IDCardvalid.html',arg)
        else:
            try:
               userContactLink=UserContactLink.objects.get(user=request.user)
            except UserContactLink.DoesNotExist:
                userContactLink=UserContactLink()
                userContactLink.user=request.user
                userContactLink.save()
            IDcardValidForm=IDCardValidForm(instance=userContactLink)
            arg['IDcardValidForm']=IDcardValidForm
            return render(request,'IDCardvalid.html',arg)
    else:
      return render(request,'login.html',arg) 
'''
学历验证
'''
def education_valid(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=='POST':
            userProfile=UserProfile.objects.get(user=request.user)
            educationValidForm=EducationValidForm(request.POST,request.FILES,instance=userProfile)
            if educationValidForm.is_valid():
                userVerification=UserVerification.objects.get(user=request.user)
                userVerification.educationPicture=educationValidForm.cleaned_data['educationPicture']
                userVerification.educationValid=2
                userProfile=educationValidForm.save(commit=False)
                userVerification.save()
                userProfile.save()
                return render(request,'verfication_success.html',arg)
            else:
                 arg['educationValidForm']=educationValidForm
                 return render(request,'educationvalid.html',arg)
        else:
            try:
               userProfile=UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                raise ValidationError('UserProfile not exist')
            educationValidForm=EducationValidForm(instance=userProfile)
            arg['educationValidForm']=educationValidForm
            return render(request,'educationvalid.html',arg)
    else:
      return render(request,'login.html',arg) 
'''
收入验证
'''
def income_valid(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=='POST':
            userProfile=UserProfile.objects.get(user=request.user)
            incomeValidForm=IncomeValidForm(request.POST,request.FILES,instance=userProfile)
            if incomeValidForm.is_valid():
                userVerification=UserVerification.objects.get(user=request.user)
                userVerification.incomePicture=incomeValidForm.cleaned_data['incomePicture']
                userVerification.incomeValid=2
                userProfile=incomeValidForm.save(commit=False)
                userVerification.save()
                userProfile.save()
                return render(request,'verfication_success.html',arg)
            else:
                 arg['incomeValidForm']=incomeValidForm
                 return render(request,'incomevalid.html',arg)
        else:
            try:
               userProfile=UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                raise ValidationError('UserProfile not exist')
            incomeValidForm=IncomeValidForm(instance=userProfile)
            arg['incomeValidForm']=incomeValidForm
            return render(request,'incomevalid.html',arg)
    else:
      return render(request,'login.html',arg) 