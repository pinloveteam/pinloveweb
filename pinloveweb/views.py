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
from django.http.response import HttpResponse, HttpResponseServerError
from apps.recommend_app.models import MatchResult
from django.db import transaction
from django.utils import simplejson
from pinloveweb.method import create_invite_code
from django.views.decorators.http import require_POST
import urllib
from util import detect_device
import os
logger = logging.getLogger(__name__)
####################
######1.0
'''
网站基本信息介绍
'''
def web(request,template_name):
    from pinloveweb.method import get_no_read_web_count
    args=get_no_read_web_count(request.user.id)
    return render(request,template_name,args)
####################

def login(request,template_name='login.html',nextUrl='/account/loggedin') :
    
    unicode_s = u'欢迎来到拼爱网'
#     if "userId" in request.COOKIES:
#         userId=request.COOKIES['userId']
#         login_in=True
# #         response.cookies['userId']['expires'] =datetime.datetime.now() + datetime.timedelta(days=14)
#     else:
#         login_in=False
    if request.user.is_authenticated() :
        return HttpResponseRedirect(nextUrl)
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
        #检测设备
        if detect_device.detectTiermobileTablet(request):
            template_name='mobile_login.html'
        return render(request, template_name, args,) 
    
def auth_view(request,template_name='login.html') : 
    args={}
    username = request.POST.get('username', '').rstrip()
    password = request.POST.get('password', '').rstrip()
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
#         logger.error('%s%s'%('0000000000000',GetLocation(request)))
        from apps.the_people_nearby.views import GetIp
#         logger.error('%s%s'%('0000003333000',GetIp(request)))
        #将个人相关信息插入缓存
        from util.cache import init_info_in_login
        init_info_in_login(user.id)
        #检测推荐信息完善情况
        from apps.recommend_app.recommend_util import recommend_info_status
        recommendStatus=recommend_info_status(request.user.id,channel='mobile' if request.path.find('/mobile/')!=-1 else 'web')
        if recommendStatus['result']:
            request.session['recommendStatus']=simplejson.dumps(recommendStatus['data'])
        #获取登录成=成功跳转地址
        from util.urls import next_url
        redirectURL = next_url(request)
        if redirectURL is None:
            url=request.path
            url='%s%s'%(url[0:(url.find('/',1))],'/loggedin/')
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(redirectURL)
    else : 
        args['user_form']= RegistrationForm()
        # Show an error page 
        args['link'] = request.REQUEST.get('link','')
        args['next'] = request.REQUEST.get('next','')
        args['error'] = True
        if len(username)==0:
           args['error_message']=u'用户名不能为空!'
        elif len(username)==0:
            args['error_message']=u'用户名不能为空!'
        else:
             args['error_message']=u'用户名或者密码错误!'
        return render(request,template_name,args)


def loggedin(request,template_name='index.html',**kwargs):
    arg={} 
    is_ajax=False
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        if request.is_ajax():
            is_ajax=True
            matchResultList=get_recommend_list(request,userProfile)
            from pinloveweb.method import load_cards_by_ajax
            return load_cards_by_ajax(request,matchResultList)
        from pinloveweb.method import get_no_read_web_count
        arg.update(get_no_read_web_count(request.user.id,fromPage=u'card'))
        #判断是否是从注册页面过来
        if request.GET.get('previous_page','')=='register':
            arg['first']=True
        #推荐信息完善
        if request.session.get('recommendStatus',False):
            arg['recommendStatus']=request.session.pop('recommendStatus')
        from pinloveweb.method import init_person_info_for_card_page
        arg.update(init_person_info_for_card_page(userProfile))
        #检测设备
        if detect_device.detectTiermobileTablet(request):
            template_name='mobile_recommend.html'
    except Exception as e:
        errorMessage='推荐页面出错,错误原因:'+e.message
        logger.exception(errorMessage)
        arg={'result':'error','error_message':errorMessage}
        template_name='error.html'
    if is_ajax:
        json=simplejson.dumps(arg)
        return HttpResponse(json)
    else:
        return render(request, template_name,arg )
    
'''
获得推荐列表
attribute：
  request：request
  flag(boolean)：是否已经生成推荐列表
  focusEachOtherList(List)：相互关注列表
  userProfile(UserProfile)：当前用户详细信息
'''
def get_recommend_list(request,userProfile,**kwargs):
    #判断推荐分数是否生成
    flag=MatchResult.objects.is_exist_by_userid(request.user.id)
    #从缓存中获取不推荐用户id
    from util.cache import get_no_recomend_list_by_cache
    disLikeUserIdList=get_no_recomend_list_by_cache(request.user.id)
    if flag:
         matchResultList=MatchResult.objects.get_match_result_by_userid(request.user.id,disLikeUserIdList)
         arg=page(request,matchResultList,**kwargs)
         matchResultList=arg['pages']
         from apps.pojo.card import matchResultList_to_CardList
         matchResultList.object_list=matchResultList_to_CardList(request.user.id,matchResultList.object_list)
    else:
          if disLikeUserIdList is None: 
              userProfileList=UserProfile.objects.filter(avatar_name_status='3').exclude(gender=userProfile.gender).exclude(user_id__in=STAFF_MEMBERS,)
          else:
              userProfileList=UserProfile.objects.filter(avatar_name_status='3').exclude(user_id__in=disLikeUserIdList).exclude(gender=userProfile.gender).exclude(user_id__in=STAFF_MEMBERS)
          arg=page(request,userProfileList,**kwargs)   
          matchResultList=arg['pages']
          from apps.pojo.card import userProfileList_to_CardList
          matchResultList.object_list=userProfileList_to_CardList(request.user.id,matchResultList.object_list)
    
    return matchResultList

     
     
def invalid_login(request) : 
    
    return render(request, 'invalid_login.html')
    
def logout(request,redirect='/') : 
    from util.cache import del_cache_in_logout
    del_cache_in_logout(request.user.id)
    auth.logout(request)
    if 'messageList' in request.session.keys():
        del request.session['messageList']
#     if "userId"  in request.COOKIES:
#             response= render(request, 'loggedout.html')
#             response.delete_cookie("userId")
#             return  response
    return HttpResponseRedirect(redirect)
    

#上传进度
def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        from django.core.cache import cache
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')
    

@transaction.commit_on_success      
def register_user(request,template_name='login.html') : 
    args = {}
    args.update(csrf(request))
    link=request.REQUEST.get('link',False)
    if link:
        args['link']=link
    if request.method == 'POST' : 
        userForm = RegistrationForm(request.POST) 
        if userForm.is_valid():
#             #判断有没邀请码
#             if request.REQUEST.get('inviteCode','')!='pinlove_fate':
#                  args['user_form']=userForm
#                  args['inviteCodeError']='输入正确的邀请码'
#                  return render(request, 'login.html', args)
            userForm.save()
            username = userForm.cleaned_data['username']
            user = User.objects.get(username=username)
            sex=userForm.cleaned_data['gender']
            from pinloveweb.method import create_register_extra_user
            create_register_extra_user(request,user.id,user.username,userForm.cleaned_data['password1'],sex,link,year_of_birth=userForm.cleaned_data['year_of_birth'],\
                                       month_of_birth=userForm.cleaned_data['month_of_birth'],day_of_birth=userForm.cleaned_data['day_of_birth'])
            authenticate = auth.authenticate(username=username, password=userForm.cleaned_data['password1'])
            auth.login(request, authenticate)
            #登录奖励
            from apps.user_score_app.method import get_score_by_invite_friend_login,get_score_by_user_login
            get_score_by_user_login(request.user.id)
            url=request.path
            url='%s%s'%(url[0:(url.find('/',1))],'/loggedin/?previous_page=register')
            #手机端做引导页面
            if url.find('/mobile/')!=-1:
                url='/mobile/update_avtar/?guide=1'
            else:
                #检测推荐信息填写情况
                from apps.recommend_app.recommend_util import recommend_info_status
                recommendStatus=recommend_info_status(request.user.id,channel='mobile' if request.path.find('/mobile/')!=-1 else 'web')
                if recommendStatus['result']:
                    request.session['recommendStatus']=simplejson.dumps(recommendStatus['data'])
            return HttpResponseRedirect(url)
        else : 
            args['user_form'] = userForm
            args['error']=True
            if userForm.errors:
                for item in userForm.errors.items():
                    key='%s%s'%(item[0],'_error')
                    args[key]=item[1][0]
    else : 
        args['user_form']= RegistrationForm() 
    return render(request, template_name, args)
    
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
def forget_password(request,template_name='forget_password.html'):
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
    return render(request, template_name,args)   
 
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

'''
下载安卓app
'''   
def android_download(request):
    args={}
    try:
        from django.core.servers.basehttp import FileWrapper
        from pinloveweb.settings import STATIC_ROOT
        file_name='pinlove_android_app.apk'
        response = HttpResponse(FileWrapper(file(('%s/download/%s'%(STATIC_ROOT,file_name)))), content_type='application/vnd.android.package-archive')
        response['Content-Disposition'] = 'attachment; filename=%s'%(file_name)
        return response
    except Exception as e:
        logger.exception('检查是否有新未读消息,出错')
        args={'result':'error','error_message':e.message}
        return render(request,'error.html',args)
        
'''
 成功页面
'''
@csrf_exempt
def success(request):
    args={}
    args['title']=request.REQUEST.get('title',None)
    args['success_message']=request.REQUEST.get('success_message',None)
    return render(request,'success.html',args)
    
def test(request):
#     from apps.task_app.tasks import task_run
#     task_run()
#     from django.utils import timezone
#     import pytz
#     pytz.common_timezones()
#     current_tz=timezone.get_current_timezone_name()
#     userProfile=UserProfile.objects.get(user=request.user)
#     from apps.recommend_app.recommend_util import cal_income
#     cal_income(userProfile.income,userProfile.gender)
   user=getattr(request,'user',None)
   from apps.third_party_login_app.forms import ConfirmInfo
   return render(request,'login_confirm_register.html',{'confirmInfo':ConfirmInfo()})
#    try:
#       import hashlib
#       chanel=hashlib.md5(simplejson.dumps({'id':request.user.id,'username':request.user.username})).hexdigest()
#       return render(request,'test.html',{'chanel':chanel})
#    except :
#       logging.exception('sdsd')
#       logger.exception("An error occurred")
#       return HttpResponse('sd')
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
    