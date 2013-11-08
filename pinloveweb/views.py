# -*- coding: utf-8 -*-

# from django.http import HttpResponse 

from django.shortcuts import render , render_to_response, redirect
from django.http import HttpResponseRedirect 
from django.contrib import auth , messages
from django.core.context_processors import csrf 

from django.contrib.auth.models import User 
from apps.user_app.models import Verification, UserVerification, Friend
from apps.user_app.models import UserProfile,UserContactLink,UserVerification,user_hobby_interest
from django.core.mail import send_mail

from forms import RegistrationForm 
from pinloveweb import settings
from apps.user_app.views import isIdAuthen, random_str
import time
from django.http.response import HttpResponse
import datetime
from django.contrib.auth.forms import UserCreationForm
from util.page import page
from django.db import connection




def login(request) :
       
    unicode_s = u'欢迎来到拼爱网'
#     if "userId" in request.COOKIES:
#         userId=request.COOKIES['userId']
#         login_in=True
# #         response.cookies['userId']['expires'] =datetime.datetime.now() + datetime.timedelta(days=14)
#     else:
#         login_in=False
    if request.user.is_authenticated() :
        return HttpResponseRedirect('/account/loggedin/')
#     if login_in:
#         response=render(request, 'loggedin.html', {'full_name': request.user.username,'set':settings.STATIC_ROOT})
#         response.set_cookie("userId",userId, max_age=60 * 60 * 24 * 7 * 2 ,expires=60 * 60 * 24 * 7 * 2 )
#         return response
    else : 
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args,) 

def auth_view(request) : 
    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if request.REQUEST.getlist('remember_status')==[u'on']:
            request.session.set_expiry(100000)
    user = auth.authenticate(username=username, password=password)
    if request.POST.get('check_save', '') !='':
        check_save=True
    else :
        check_save=False
    if user is not None and user.is_active : 
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page 
        if check_save:
            response= render(request, 'loggedin.html', {'full_name': request.user.username,'set':settings.STATIC_ROOT})
            response.set_cookie("userId",user.id, max_age=60 * 60 * 24 * 7 * 2 ,expires=60 * 60 * 24 * 7 * 2 )
            return response
        elif  "userId"  in request.COOKIES:
            response= render(request, 'loggedin.html', {'full_name': request.user.username,'set':settings.STATIC_ROOT})
            response.delete_cookie("userId")
            return response
        return HttpResponseRedirect('/account/loggedin/')
    else : 
        # Show an error page 
        return HttpResponseRedirect('/account/invalid/')

def loggedin(request) : 
  arg={}
  if request.user.is_authenticated():
    from apps.recommend_app.models import MatchResult
    #判断推荐分数是否生成
    count=MatchResult.objects.filter(my_id=request.user.id).count()
    userProfile=UserProfile.objects.get(user_id=request.user.id)
    #关注
    myFollow=Friend.objects.filter(my=request.user).count()
    otherFollow=Friend.objects.filter(friend=request.user).count()
    sql="select my_id from user_app_friend where friend_id="+str(request.user.id)+" and my_id in (SELECT friend_id from user_app_friend where my_id="+str(request.user.id)+") "
    cursor=connection.cursor();
    cursor.execute(sql)
    follow=cursor.fetchall()
    
    if count>0:
         matchResultList=MatchResult.objects.select_related().filter(my_id=request.user.id)
         arg=page(request,matchResultList)
         matchResultList=arg['pages']
         from apps.recommend_app.views import matchResultList_to_RecommendResultList
         matchResultList.object_list=matchResultList_to_RecommendResultList(matchResultList.object_list)
         friends = Friend.objects.filter(my_id=request.user.id)
         i=0 
         for user in matchResultList:
           for friend in friends:
               if user.user_id == friend.friend_id:
                   if  user.user_id in follow:
                       matchResultList[i].isFriend=2
                   else:
                       matchResultList[i].isFriend=1
           i+=1
         arg['pages']=matchResultList
    else:
          userProfileList=UserProfile.objects.exclude(user=request.user).exclude(gender=userProfile.gender).order_by("?")
          arg=page(request,userProfileList)   
          matchResultList=arg['pages']
          from apps.recommend_app.views import userProfileList_to_RecommendResultList
          matchResultList.object_list=userProfileList_to_RecommendResultList(matchResultList.object_list)
          friends = Friend.objects.select_related().filter(my=request.user)
          i=0 
          attentionEachOther=[]
          for f in follow:  
              attentionEachOther.append(f[0])
          for user in matchResultList:
           for friend in friends:
               if user.user_id == friend.friend_id:
                   if  user.user_id in attentionEachOther:
                       matchResultList[i].isFriend=2
                   else:
                       matchResultList[i].isFriend=1
           i+=1
          arg['pages']=matchResultList
    
    arg=init_card(arg,userProfile)
    arg['myFollow']=myFollow
    arg['otherFollow']=otherFollow
    arg['follow']=len(follow)  
    return render(request, 'card.html',arg )
  else:
    return render(request,'login.html',arg)
#用于初始化card页面所需要的信息
def init_card(arg,userProfile):
    if userProfile.avatar_name_status!='3':
        arg['avatar_name']='user_img/image.png'
    else:
        arg['avatar_name']=userProfile.avatar_name
    arg['age']=userProfile.age
    arg['height']=userProfile.height
    arg['income']=userProfile.income
    arg['education']=userProfile.get_education_display()
    arg['jobIndustry']=userProfile.get_jobIndustry_display()
    return arg
     
     
def invalid_login(request) : 
    
    return render(request, 'invalid_login.html')
    
def logout(request) : 
    
    auth.logout(request)
#     if "userId"  in request.COOKIES:
#             response= render(request, 'loggedout.html')
#             response.delete_cookie("userId")
#             return  response
    return HttpResponseRedirect("/account/loggedout/")
    
def loggedout(request) : 
    
    return render(request, 'loggedout.html')
    
def register_user(request) : 
    
    args = {}
    args.update(csrf(request))
    
    if request.method == 'POST' : 
        userForm = RegistrationForm(request.POST) 
        check_box_list = request.REQUEST.getlist('check_box_list')
        if userForm.is_valid() and len(check_box_list):
            userForm.save()
            
            username = userForm.cleaned_data['username']
            # password = user_form.clean_password2()
            # user = authenticate(username=username, password=password)
            user = User.objects.get(username=username)
            user.is_active = False 
            #user verification
            user_code = random_str()
            verification = Verification()
            verification.username = username
            verification.verification_code = user_code
            verification.save()
            sex=userForm.cleaned_data['gender']
            userForm.photo='user_img/image.png'
            UserProfile(user_id=user.id,gender=sex).save()
            #创建用户验证信息
            userVerification=UserVerification()
            userVerification.user=user
            userVerification.save()
            # we need to generate a random number as the verification key 
            
            # user needs email verification 
            domain_name = u'http://www.pinpinlove.com/account/verification/'
            email_verification_link = domain_name + '?username=' + username + '&' + 'user_code=' + user_code
            
            email_message = u"请您点击下面这个链接完成注册："
            email_message += email_verification_link
            try :
               from pinloveweb.settings import DEFAULT_FROM_EMAIL
               send_mail(u'拼爱网注册电子邮件地址验证', email_message,DEFAULT_FROM_EMAIL,[user.email]) 
            except:
                print u'邮件发送失败'
                pass
            
            # login(request, user)
            return render_to_response('register_email_verification.html',{'username':username, 'email': user.email})
            
            #return HttpResponseRedirect('/account/register_verify/')
            # return HttpResponseRedirect('/account/register_success/') 
        else : 
            args['user_form'] = userForm

    else : 
        args['user_form']= RegistrationForm() 
    
    return render(request, 'register.html', args)
    
def register_success(request) : 
    return render(request, 'register_success.html')
    
def register_verify(request) : 
    username = request.REQUEST.get('username','')
#     user_code = request.REQUEST.get('user_code','')
    user = User.objects.get(username=username)
#     verification = Verification.objects.get(username=username)
    if isIdAuthen(request):
        user.is_active = True 
        UserVerification.objects.filter(user=user).update(emailValid='2')
#         verification.delete()
        return render(request, 'register_success.html')
    else :
        return render(request, 'error.html')

def forget_password(request) : 
    return render(request, 'forget_password.html')   
 
                          
                          