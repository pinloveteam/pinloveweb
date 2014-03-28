# -*- coding: utf-8 -*-

# from django.http import HttpResponse 

from django.shortcuts import render , render_to_response, redirect
from django.http import HttpResponseRedirect 
from django.contrib import auth , messages
from django.core.context_processors import csrf 

from django.contrib.auth.models import User 
from apps.user_app.models import Verification, UserVerification, Follow
from apps.user_app.models import UserProfile,UserContactLink,UserVerification
from django.core.mail import send_mail

from forms import RegistrationForm 
from pinloveweb import settings
from apps.user_app.views import isIdAuthen
import time
import datetime
from django.contrib.auth.forms import UserCreationForm
from util.page import page
from django.db import connection
from apps.the_people_nearby.views import GetLocation
import logging
from django.views.decorators.csrf import csrf_protect
from django.http.response import HttpResponse
from apps.recommend_app.models import MatchResult




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
        redirectURL=request.REQUEST.get('redirectURL','')
        if redirectURL!='':
            args['redirectURL']=redirectURL
        args.update(csrf(request))
        return render(request, 'login.html', args,) 
    
@csrf_protect
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
        #获取ip 地址
        UserProfile.objects.filter(user=request.user).update(lastLoginAddress=GetLocation(request))
        #获取登录成=成功跳转地址
        from util.urls import next_url
        redirectURL = next_url(request)
        if redirectURL is None:
            return HttpResponseRedirect('/account/loggedin/')
        else:
            return HttpResponseRedirect(redirectURL)
    else : 
        # Show an error page 
        return HttpResponseRedirect('/account/invalid/')
'''
根据key 获取缓存数据
'''
def get_cache_by_key(key):
    cache_key = key
    from django.core.cache import cache
    data = cache.get(cache_key)
    return data

def loggedin(request,**kwargs) :
    arg={} 
    #判断推荐分数是否生成
    flag=MatchResult.objects.is_exist_by_userid(request.user.id)
    userProfile=UserProfile.objects.get_user_info(request.user.id)
    #相互关注的人的id
    follows=Follow.objects.follow_each(request.user.id)
    focusEachOtherList=[follow.my.id for follow in follows ]
    #从缓存中获取不推荐用户id
    disLikeUserIdList=get_cache_by_key(request.user.id)
    #获取推荐列表
    matchResultList=get_recommend_list(request,flag,disLikeUserIdList,focusEachOtherList,userProfile,**kwargs)
    if kwargs.get('card')==True:
        return matchResultList
    if request.GET.get('ajax')=='true':
        from pinloveweb.method import load_cards_by_ajax
        return load_cards_by_ajax(request,matchResultList)
    from apps.pojo.card import MyEncoder
    from django.utils import simplejson
    matchResultList.object_list=simplejson.dumps(matchResultList.object_list,cls=MyEncoder)
    arg['pages']=matchResultList
    from pinloveweb.method import init_person_info_for_card_page
    arg.update(init_person_info_for_card_page(userProfile,followEachCount=len(focusEachOtherList)))
    return render(request, 'card.html',arg )

'''
获得推荐列表
attribute：
  request：request
  flag(boolean)：是否已经生成推荐列表
  focusEachOtherList(List)：相互关注列表
  userProfile(UserProfile)：当前用户详细信息
'''
def get_recommend_list(request,flag,disLikeUserIdList,focusEachOtherList,userProfile,**kwargs):
    if flag:
         if disLikeUserIdList is None:
             matchResultList=MatchResult.objects.select_related('other').filter(my_id=request.user.id)
         else:
            matchResultList=MatchResult.objects.select_related('other').filter(my_id=request.user.id).exclude(other_id__in=disLikeUserIdList)
         arg=page(request,matchResultList,**kwargs)
         matchResultList=arg['pages']
         from apps.pojo.card import matchResultList_to_CardList
         matchResultList.object_list=matchResultList_to_CardList(matchResultList.object_list)
    else:
          if disLikeUserIdList is None: 
              userProfileList=UserProfile.objects.exclude(gender=userProfile.gender)
          else:
              userProfileList=UserProfile.objects.exclude(user_id__in=disLikeUserIdList).exclude(gender=userProfile.gender)
          arg=page(request,userProfileList,**kwargs)   
          matchResultList=arg['pages']
          from apps.pojo.card import userProfileList_to_CardList
          matchResultList.object_list=userProfileList_to_CardList(matchResultList.object_list)
    from pinloveweb.method import is_focus_each_other
    matchResultList=is_focus_each_other(request,matchResultList,focusEachOtherList)
    return matchResultList

     
     
def invalid_login(request) : 
    
    return render(request, 'invalid_login.html')
    
def logout(request) : 
    
    auth.logout(request)
    if 'messageList' in request.session.keys():
        del request.session['messageList']
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
            from util.util import random_str
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
            auth.authenticate(username=username, password=user.password)
            return HttpResponseRedirect('/account/loggedin/')
            
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
 
                          
def test(request):
    from django.core.cache import cache
    cache_key = "myID"
    result = cache.get(cache_key)
    if result is None:
        data = "hello, found"
        cache.set(cache_key, data, 60)
        return HttpResponse("not found")
    else:
        return HttpResponse(result)
    