# -*- coding: utf-8 -*-

# from django.http import HttpResponse 

from django.shortcuts import render 
from django.http import HttpResponseRedirect 
from django.contrib import auth 
from django.core.context_processors import csrf 

from django.contrib.auth.models import User 
from apps.user_app.models import  UserVerification, Verification
from apps.user_app.models import UserProfile

from forms import RegistrationForm 
from pinloveweb import settings, STAFF_MEMBERS
from apps.user_app.views import isIdAuthen
from util.page import page
from apps.the_people_nearby.views import GetLocation
import logging
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http.response import HttpResponse
from apps.recommend_app.models import MatchResult
from django.db import transaction
from django.utils import simplejson
from pinloveweb.method import create_invite_code
from django.views.decorators.http import require_POST
logger = logging.getLogger(__name__)
####################
######1.0
'''
网站基本信息介绍
'''
def web(request,template_name):
    return render(request,template_name,)
####################

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
        args['user_form']= RegistrationForm() 
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
        #登录奖励
        from apps.user_score_app.method import get_score_by_invite_friend_login,get_score_by_user_login
        get_score_by_user_login(request.user.id)
        #邀请
        link=request.REQUEST.get('link',False)
        #内存里初始化个人相关信息
        from util.cache import init_profile_into_cache
        init_profile_into_cache(user.id)
        if link:
            get_score_by_invite_friend_login(link,request.user.id)
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
        link = request.REQUEST.get('link','')
        next = request.REQUEST.get('next','')
        return render(request,'login.html',{'error':'True','error_message':'用户名或者密码错误!','link':link,'next':next,'user_form':RegistrationForm()},)
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
    #从缓存中获取不推荐用户id
    disLikeUserIdList=get_cache_by_key(request.user.id)
    #获取推荐列表
    matchResultList=get_recommend_list(request,flag,disLikeUserIdList,userProfile,**kwargs)
    if kwargs.get('card')==True:
        return matchResultList
    if request.GET.get('ajax')=='true':
        from pinloveweb.method import load_cards_by_ajax
        return load_cards_by_ajax(request,matchResultList)
    from apps.pojo.card import MyEncoder
    from django.utils import simplejson
    matchResultList.object_list=simplejson.dumps(matchResultList.object_list,cls=MyEncoder)
    arg['pages']=matchResultList
    #判断是否是从注册页面过来
    if request.GET.get('previous_page','')=='register':
        arg['first']=True
    from pinloveweb.method import init_person_info_for_card_page
    arg.update(init_person_info_for_card_page(userProfile))
    return render(request, 'index.html',arg )

'''
获得推荐列表
attribute：
  request：request
  flag(boolean)：是否已经生成推荐列表
  focusEachOtherList(List)：相互关注列表
  userProfile(UserProfile)：当前用户详细信息
'''
def get_recommend_list(request,flag,disLikeUserIdList,userProfile,**kwargs):
    if flag:
         matchResultList=MatchResult.objects.get_match_result_by_userid(request.user.id,disLikeUserIdList)
         arg=page(request,matchResultList,**kwargs)
         matchResultList=arg['pages']
         from apps.pojo.card import matchResultList_to_CardList
         matchResultList.object_list=matchResultList_to_CardList(request.user.id,matchResultList.object_list)
    else:
          if disLikeUserIdList is None: 
              userProfileList=UserProfile.objects.exclude(gender=userProfile.gender, avatar_name_status='3').exclude(user_id__in=STAFF_MEMBERS,)
          else:
              userProfileList=UserProfile.objects.exclude(user_id__in=disLikeUserIdList).exclude(gender=userProfile.gender, avatar_name_status='3').exclude(user_id__in=STAFF_MEMBERS)
          arg=page(request,userProfileList,**kwargs)   
          matchResultList=arg['pages']
          from apps.pojo.card import userProfileList_to_CardList
          matchResultList.object_list=userProfileList_to_CardList(request.user.id,matchResultList.object_list)
    
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

@transaction.commit_on_success      
def register_user(request) : 
    args = {}
    args.update(csrf(request))
    link=request.REQUEST.get('link',False)
    if link:
        args['link']=link
    if request.method == 'POST' : 
        userForm = RegistrationForm(request.POST) 
        if userForm.is_valid():
            #判断有没邀请码
            if request.REQUEST.get('inviteCode','')!='pinlove_fate':
                 args['user_form']=userForm
                 args['inviteCodeError']='输入正确的邀请码'
                 return render(request, 'register.html', args)
            userForm.save()
            username = userForm.cleaned_data['username']
            user = User.objects.get(username=username)
            sex=userForm.cleaned_data['gender']
            #创建二维码
            Userlink=create_invite_code(user.id)
            UserProfile(user_id=user.id,gender=sex,link=Userlink).save()
            #生成激活码
            from util.util import random_str
            user_code = random_str()
            #初始化所需表
            from pinloveweb.method import init_table_in_register
            init_table_in_register(user,user_code)
            #注册成功赠送积分
            from apps.user_score_app.method import get_score_by_invite_friend_register
            if link:
                get_score_by_invite_friend_register(link)
            user = auth.authenticate(username=username, password=userForm.cleaned_data['password1'])
            auth.login(request, user)
            #内存里初始化个人相关信息
            from util.cache import init_profile_into_cache
            init_profile_into_cache(user.id)
            return HttpResponseRedirect('/account/loggedin/?previous_page=register')
        else : 
            args['user_form'] = userForm
            args['error']=True
            if userForm.errors:
                for item in userForm.errors.items():
                    key='%s%s'%(item[0],'_error')
                    args[key]=item[1][0]
    else : 
        args['user_form']= RegistrationForm() 
    
    return render(request, 'login.html', args)
    
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

'''
忘记密码
'''
def forget_password(request):
    args={}
    #是否出错
    flag=True
    #是否提交请求
    postResult=False
    if request.method == 'POST':
         querystr = request.REQUEST.get('forget_account','')
         user = User()
         if request.REQUEST.get('forget_type','') == 'email':
            try :
               user = User.objects.get(email=querystr)
            except Exception:
                args['error_message']='该邮箱未注册!'
                flag=False
                pass
         elif request.REQUEST.get('forget_type','') == 'username':
             try :
               user = User.objects.get(username=querystr)
             except Exception:
               args['error_message']='该用户未注册!'
               flag=False
               pass
         else :
            return render(request, 'error.html') 
         if flag:
            if Verification.objects.filter(username=user.username).exists():
                Verification.objects.filter(username=user.username).delete()
            verification = Verification()
            verification.username = user.username
            from apps.verification_app.views import random_str
            user_code=random_str() 
            verification.verification_code = user_code
            verification.save()
            #发送邮件
            from pinloveweb.method import send_reset_password
            send_reset_password(user,user_code)
            args['email']=user.email
            postResult=True
    args['postResult']=postResult
    return render(request, 'forget_password.html',args)   
 
'''
注册检查
'''
def check_register(request):
    args={}
    try:
        if request.GET.get('type','')==u'check_username':
            username=request.GET.get('username','')
            if User.objects.filter(username=username).exists():
                args={'result':u'error','error_message':u'用户名已存在!'}
            else:
                args['result']=u'success'
        elif request.GET.get('type','')==u'check_email':
            email=request.GET.get('email','')
            if User.objects.filter(email=email).exists():
                args={'result':u'error','error_message':u'邮箱已存在!'}
            else:
                args['result']=u'success'
        
    except Exception as e:
        pass
    json=simplejson.dumps(args)
    return HttpResponse(json)
                          
'''
检查是否有新未读消息，有则返回数量
@param from: card页面，  message页面
'''                      
def newcount(request):
    args={}
    try:
        userId=request.user.id
        fromPage=request.REQUEST.get('from',False)
        #获取未读信息
        from pinloveweb.method import get_no_read_web_count
        args=get_no_read_web_count(userId,fromPage=fromPage)
        args['result']='success'
    except Exception,e:
        logger.exception('检查是否有新未读消息,出错')
        args['result']='error'
    json=simplejson.dumps(args)
    return HttpResponse(json)
    
def test(request):
   try:
      import hashlib
      chanel=hashlib.md5(simplejson.dumps({'id':request.user.id,'username':request.user.username})).hexdigest()
      return render(request,'test.html',{'chanel':chanel})
   except :
      logging.exception('sdsd')
      logger.exception("An error occurred")
      return HttpResponse('sd')
############################
@require_POST
@csrf_exempt
def pusher_authentication(request):
    socket_id=request.POST.get('socket_id')
    channel_name=request.POST.get('channel_name')
    APP_ID='82042'
    APP_KEY='96c2a47c4f074b2cc22e'
    APP_SECRET ='f90fc229ede97d99a3a8'
    from pinloveweb.method import sign_channel
    md5=sign_channel(request)
    if channel_name=='%s%s'%(u'private_',md5):
        import pusher
        p = pusher.Pusher(app_id=APP_ID, key=APP_KEY, secret=APP_SECRET)
        auth = p[channel_name].authenticate(socket_id)
        json=simplejson.dumps(auth)
        return HttpResponse(json)
    
    
    