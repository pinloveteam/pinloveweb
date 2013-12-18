# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2013

@author: jin
'''
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
import logging
import simplejson
from apps.user_app.models import UserProfile
import datetime
from .setting import (
     QQAPPID,
     QQAPPKEY,
     SinaAppKey,
     SinaAppSercet,
     SINA_CALLBACK_URL,
     QQ_CALLBACK_URL,
     FaceBookAppID,
     FaceBookAppSecret,
     FACEBOOK_CALLBACK_URL,
     TwitterConsumerKey,
     TwitterConsumerSecret,
     TWITTER_CALLBACK_URL,
     )
from apps.third_party_login_app.setting import DEFAULT_PASSWORD
from django.shortcuts import render
log=logging.getLogger('customapp.engine')

##########three paerty login######
'''
获取qq授权登录地址,跳转到回调地址（redirect_uri）
'''   
def get_qq_login_url(request):     
    from apps.third_party_login_app.openqqpy import OpenQQClient
    client = OpenQQClient(client_id=QQAPPID,client_secret=QQAPPKEY,redirect_uri=QQ_CALLBACK_URL)
    #获取qq授权登录地址
    return HttpResponseRedirect(client.get_auth_url())  

'''
获取qq信息并登录个人主页
'''
def qq_login(request):
    from apps.third_party_login_app.setting import DEFAULT_PASSWORD
    from apps.third_party_login_app.openqqpy import OpenQQClient
    client = OpenQQClient(client_id=QQAPPID,client_secret=QQAPPKEY,redirect_uri='http://snailjin.eicp.net/',scope='')
    log.error(request.GET.get('code'))
    access=client.request_access_token(request.GET.get('code')) #返回access_token,expires_in
    access_token=access['access_token']
    expires_in=access['expires_in']
    request.session['access_token']=access_token
    request.session['expires_in']=expires_in
    client.set_access_token( access_token,expires_in )
    openid=client.request_openid() #返回openid
    #判断是否有第三方登录过
    from apps.third_party_login_app.models import ThirdPsartyLogin
    if not ThirdPsartyLogin.objects.filter(provider='0',uid=openid).exists():
        client.set_openid(openid)
        user_info=client.request_api('user/get_user_info')
        #判断是否获取错误
        if user_info['ret']==0:
            #创建用户
            user=create_user(user_info['nickname'].strip())
            #创建第三方登录表信息
            ThirdPsartyLogin(user=user,provider='0',uid=openid,access_token=access_token).save()
            #创建用户详细信息
            create_user_profile(user,user_info['gender'])
            #登录
            login(request,user.username,DEFAULT_PASSWORD)
    else:
        #根据QQopenId获取用户信息
        user=ThirdPsartyLogin.objects.get(provider='0',uid=openid).user
        login(request,user.username,DEFAULT_PASSWORD)
    return HttpResponseRedirect('/account/loggedin/')
       
'''
获取sina授权登录地址,跳转到回调地址（redirect_uri）
'''
def sina_login_url(request):
    from apps.third_party_login_app.weibo import APIClient
    client = APIClient(app_key=SinaAppKey, app_secret=SinaAppSercet, redirect_uri=SINA_CALLBACK_URL)
    url = client.get_authorize_url()
    log.error('%s%s' %('url====',url))
    return HttpResponseRedirect(url)

'''
获取sina信息并登录个人主页
'''
def sina_login(request):
    try:
        code=request.REQUEST.get('code','')
        if code=='':
            raise Exception("不能获取code值")
    except Exception, e:
        print e
    from apps.third_party_login_app.weibo import APIClient
    client = APIClient(app_key=SinaAppKey, app_secret=SinaAppSercet, redirect_uri=SINA_CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token # 新浪返回的token，类似abc123xyz456
    expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    uid=r.uid
    # TODO: 在此可保存access token
    client.set_access_token(access_token, expires_in)
    request.session['access_token']=access_token
    request.session['expires_in']=expires_in
#     log.error('access_token===='+access_token)
#     log.error('expires_in====='+str(expires_in))
#     log.error('uid====='+str(uid))
    from apps.third_party_login_app.models import ThirdPsartyLogin
    if not ThirdPsartyLogin.objects.filter(provider='1',uid=uid).exists():
            #获取用户信息
            user_info=client.users.show.get(uid=uid)
            #创建用户
            user=create_user(user_info['screen_name'].strip())
            #创建第三方登录表信息
            ThirdPsartyLogin(user=user,provider='1',uid=uid,access_token=access_token).save()
            #创建用户详细信息
            create_user_profile(user,user_info['gender'],)
            #登录
            from apps.third_party_login_app.setting import DEFAULT_PASSWORD
            login(request,user.username,DEFAULT_PASSWORD)
    else:
        #根据QQopenId获取用户信息
        user=ThirdPsartyLogin.objects.get(provider='1',uid=uid).user
        login(request,user.username,DEFAULT_PASSWORD)
    return HttpResponseRedirect('/account/loggedin/')

    user_info=client.users.show.get(uid=uid)
    return HttpResponse(user_info['screen_name'])

'''
获取facebook授权登录地址,跳转到回调地址（redirect_uri）
'''
def facebook_login_url(request):
    from apps.third_party_login_app.facebook import auth_url
    url=auth_url(FaceBookAppID,FACEBOOK_CALLBACK_URL)
    log.error('%s%s' %('url====',url))
    return HttpResponseRedirect(url)

def facebook_login(request):
    from apps.third_party_login_app.facebook import get_access_token_from_code
    access=get_access_token_from_code(request.GET['code'],FACEBOOK_CALLBACK_URL, FaceBookAppID, FaceBookAppSecret)
    access_token=access['access_token']  #facebook返回的token
    expires_in=access['expires']    #token过期时间
    request.session['access_token']=access_token
    request.session['expires_in']=expires_in
    from apps.third_party_login_app import facebook
    graph = facebook.GraphAPI(access_token)
    user_info = graph.get_object('me')
    from apps.third_party_login_app.models import ThirdPsartyLogin
    if not ThirdPsartyLogin.objects.filter(provider='2',uid=user_info['id']).exists():
            #创建用户
            user=create_user(user_info['name'].strip(),
                             firstName=user_info['first_name'].strip(),
                             lastName=user_info['last_name'].strip(),
                             )
            #创建第三方登录表信息
            ThirdPsartyLogin(user=user,provider='2',uid=user_info['id'],access_token=access_token).save()
            #创建用户详细信息
            create_user_profile(user,user_info['gender'].strip(),country=user_info['locale'],)
            #登录
            login(request,user.username,DEFAULT_PASSWORD)
    else:
        #根据QQopenId获取用户信息
        user=ThirdPsartyLogin.objects.get(provider='2',uid=user_info['id']).user
        login(request,user.username,DEFAULT_PASSWORD)
    return HttpResponseRedirect('/account/loggedin/')


'''
获取twitter授权登录地址,跳转到回调地址（redirect_uri）
'''
def twitter_login_url(request):
    from apps.third_party_login_app.twython.api import Twython
    twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret)
    auth = twitter.get_authentication_tokens(callback_url=TWITTER_CALLBACK_URL)
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
#     log.error('OAUTH_TOKEN==='+OAUTH_TOKEN)
#     log.error('OAUTH_TOKEN_SECRET==='+OAUTH_TOKEN_SECRET)
    request.session['OAUTH_TOKEN']=OAUTH_TOKEN
    request.session['OAUTH_TOKEN_SECRET']=OAUTH_TOKEN_SECRET
    return HttpResponseRedirect(auth['auth_url'])

def twitter_login(request):
#     log.error('OAUTH_TOKEN111==='+request.GET.get('oauth_token'))
    from apps.third_party_login_app.twython.api import Twython
    twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret,request.session['OAUTH_TOKEN'],request.session['OAUTH_TOKEN_SECRET'])
    get_user_info = twitter.get_authorized_tokens(request.GET['oauth_verifier'])
    return HttpResponse(get_user_info['screen_name'])
    
''''
用户登录并且获得本机ip
attribute：
     用户名:username
  密  码    : password
'''   
def login(request,username,password):
     from django.contrib import auth
     user = auth.authenticate(username=username, password=password)
     log.error(username+'   '+password)
     if user is not None and user.is_active : 
         auth.login(request, user)
         log.error("login success"+request.user.username+'fcsdfsf')
     from apps.the_people_nearby.views import GetLocation
     if not GetLocation(request)==None:
         UserProfile.objects.filter(user=request.user).update(lastLoginAddress=GetLocation(request))
     
           
'''
为第三方登录创建用户
attribute:
    username:用户名
    fristName 
    lastName
return
   user
'''
def create_user(username,**kwarg):
    from django.contrib.auth.hashers import make_password
    user=User()
    user.username=username
    if kwarg.get('firstName')!=None:
        user.first_name=kwarg.get('firstName')
    if  kwarg.get('lastName')!=None:
        user.last_name=kwarg.get('lastName')
    from apps.third_party_login_app.setting import DEFAULT_PASSWORD
    user.password=make_password(DEFAULT_PASSWORD)
    user.is_active=True
    user.date_joined=datetime.datetime.today()
    user.last_login= datetime.datetime.today()
    user.save()
    return user

'''
为第三方用户创建用户信息信息
'''
def create_user_profile(user,gender,**kwarg):
    userProfile=UserProfile(user=user)
    genderList=['m',u"男",'male']
    if gender in genderList:
        userProfile.gender='F'
    else:
        userProfile.gender='M'
    if kwarg.get('country')!=None:
        if kwarg.get('country')=='zh_CN':
            userProfile.country=='中国'
    userProfile.save()
    
##########other action######

def get_facebook_friend_list(request):
    import time
    if 'expires_in' in request.session.keys() and time.time()<request.session['expires_in']:
        access_token=request.session['access_token']
        from apps.third_party_login_app import facebook
        graph = facebook.GraphAPI(access_token)
        friends = graph.get_friends()
        return render(request,'facebook_friend_list.html',{'friends':friends})
    else:
         return facebook_login_url(request)
def has_permissions(request):
    import time
    if 'expires_in' in request.session.keys() and time.time()<request.session['expires_in']:
         access_token=request.session['access_token']
         from apps.third_party_login_app import facebook
         graph = facebook.GraphAPI(access_token)
         graph.permissions()
         if graph.has_permissions(['publish_stream',]):
             facebook_feeds(request)
         else:
             from apps.third_party_login_app.facebook import auth_url
             from apps.third_party_login_app.setting import WEB_ROOT
             url=auth_url(FaceBookAppID,WEB_ROOT+'/third_party_login/facebook_feeds/',perms='publish_stream',)
             return HttpResponseRedirect(url)
    else:
         return facebook_login_url(request)

def facebook_feeds(request):
    if request.method=='POST':
        access_token=request.session['access_token']
        import time
        if 'expires_in' in request.session or time.time()<request.session['expires_in']:
            from apps.third_party_login_app import facebook
            graph = facebook.GraphAPI(access_token)
            graph.permissions()
            graph.has_permissions(['user_friends',])
            return HttpResponse('发送成功！')
        else:
            return facebook_login_url(request)
    else:
        return render(request,'facebook_feed.html')
        