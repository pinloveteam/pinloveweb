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
from django.views.decorators.csrf import csrf_exempt
from apps.third_party_login_app.models import FacebookUser, FacebookPhoto
import urllib2
from django.utils import simplejson
log=logging.getLogger(__name__)

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
    from apps.third_party_login_app.openqqpy import OpenQQClient
    client = OpenQQClient(client_id=QQAPPID,client_secret=QQAPPKEY,redirect_uri=QQ_CALLBACK_URL,scope='')
#     log.error(request.GET.get('code'))
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
#     log.error('%s%s' %('url====',url))
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
@csrf_exempt
def facebook_login_url(request):
    from apps.third_party_login_app.facebook import auth_url
    url=auth_url(FaceBookAppID,FACEBOOK_CALLBACK_URL)
#     log.error('%s%s' %('url====',url))
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
    auth = twitter.get_authentication_tokens()
    request.session['request_token'] = auth
#     log.error('OAUTH_TOKEN==='+request.session['OAUTH_TOKEN'])
#     log.error('OAUTH_TOKEN_SECRET==='+request.session['OAUTH_TOKEN'])
    return HttpResponseRedirect(auth['auth_url'])

def twitter_login(request):
    from apps.third_party_login_app.twython.api import Twython
    oauth_token = request.session['request_token']['oauth_token']
    oauth_token_secret = request.session['request_token']['oauth_token_secret']
    twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret,oauth_token,oauth_token_secret)
    authorized_tokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'])
    OAUTH_TOKEN = authorized_tokens['oauth_token']
    OAUTH_TOKEN_SECERT = authorized_tokens['oauth_token_secret']
    request.session['OAUTH_TOKEN']=OAUTH_TOKEN
    request.session['OAUTH_TOKEN_SECRET']=OAUTH_TOKEN_SECERT
    twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret,OAUTH_TOKEN,OAUTH_TOKEN_SECERT)
    log.error('session=='+request.session['OAUTH_TOKEN']+",,,,"+request.session['OAUTH_TOKEN_SECRET'])
    user_info=twitter.verify_credentials()
    from apps.third_party_login_app.models import ThirdPsartyLogin
    if not ThirdPsartyLogin.objects.filter(provider='4',uid=user_info['id']).exists():
            #创建用户
            user=create_user(user_info['screen_name'].strip(),
                             )
            #创建第三方登录表信息
            ThirdPsartyLogin(user=user,provider='4',uid=user_info['id'],access_token='%s%s%s'% (request.session['OAUTH_TOKEN'],'|',request.session['OAUTH_TOKEN_SECRET'])).save()
            #创建用户详细信息
            create_user_profile(user,None)
            login(request,user.username,DEFAULT_PASSWORD)
            #选择性别
            return render(request,'chose_gender.html')
    else:
        #根据QQopenId获取用户信息
        user=ThirdPsartyLogin.objects.get(provider='4',uid=user_info['id']).user
        login(request,user.username,DEFAULT_PASSWORD)
    return HttpResponseRedirect('/account/loggedin/')
 
def update_gender(request):
    gender=request.POST.get('gender')
    UserProfile.objects.filter(user=request.user).update(gender=gender)
    return HttpResponseRedirect('/account/loggedin/')
       
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
#          log.error("login success"+request.user.username+'fcsdfsf')
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
        userProfile.gender='M'
    else:
        userProfile.gender='F'
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
    
from apps.third_party_login_app.django_facebook.decorators import canvas_only
@csrf_exempt
@canvas_only
def pintu_for_facebook(request):
    uid=request.facebook.user.get('uid')
    request.session['graph']=request.facebook.graph
    args=init_pintu(request,uid)
    for field in ['data','inviteNonfirmList']:
        args[field]=simplejson.dumps(args[field])
    return render(request, 'pintu_for_facebook.html',args)
#     facebookUserList=[{'username': u'Love  Pin', 'location': u'Hangzhou, China', 'online': 1, 'uid': u'100007247470289', 
#      'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/t1/c28.0.80.80/p80x80/1476022_1382326562018913_1553944026_n.jpg','smallAvatar':'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t5/211329_100007247470289_259768164_q.jpg'}]
#     users=[{'username': u'Love  Pin', 'uid': u'100007247470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#            {'username': u'Love  n', 'uid': u'100007247470234', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#            {'username': u'Lov  Pin', 'uid': u'1000072470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'}]
#     inviteNonfirmList=[{'username': u'Love  Pin', 'uid': u'100007247470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#            {'username': u'Love  n', 'uid': u'100007247470234', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#            {'username': u'Lov  Pin', 'uid': u'1000072470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#            {'username': u'Lov  Pin', 'uid': u'1000072470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#                       { 'username': u'Lov  Pin', 'uid': u'1000072470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#                        {'username': u'Lov  Pin', 'uid': u'1000072470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#                        {'username': u'Lov  Pin', 'uid': u'1000072470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'},
#                        {'username': u'Lov  Pin', 'uid': u'1000072470289', 'avatar': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg'}]
#     from apps.game_app.models import get_recommend_history
#     facebookUserRecordList=get_recommend_history('100007203789389')
#     return render(request, 'pintu_for_facebook.html',{'uid':'100007203789389','count':10,'data':simplejson.dumps(users),'userCount':len(users),'inviteNonfirmList':simplejson.dumps(inviteNonfirmList),'facebookUserRecordList':facebookUserRecordList})
    
'''
 初始化页面
''' 
def pintu_for_facebook_android(request):
    try:
        callback = request.GET.get('callback')
        uid=request.GET.get('uid',False)
        expiresIn=float(request.GET.get('expiresIn',False))
        accessToken=request.GET.get('accessToken',False)
        if not (uid and expiresIn and expiresIn):
            json=callback + '('+simplejson.dumps({'result':'error'})+')'
            return HttpResponse(json)
    except Exception:
        log.error('android 登录取参数出错！')
        json=callback + '('+simplejson.dumps({'result':'error'})+')'
        return HttpResponse(json)
    from apps.third_party_login_app.django_facebook.middleware import DjangoFacebook
    user = {
            'uid':uid,
            'access_token': accessToken,
            'expires':expiresIn
        }
    request.facebook = DjangoFacebook(user)
    request.session['graph']= request.facebook.graph
    args=init_pintu(request,uid)
    args['result']='success'
    json=callback + '('+simplejson.dumps(args)+')'
    return HttpResponse(json)
'''
初始facebook拼图页面
'''
def init_pintu(request,uid):
    args={}
    args['uid']=uid
#     data=request.facebook.graph.extend_access_token( FaceBookAppID,FaceBookAppSecret)
    if FacebookUser.objects.filter(uid=uid).exists():
        me=request.facebook.user
    else:
        facebook_save(request,uid)
#         feed(request)
    #获取游戏次数
    from apps.game_app.models import get_count,get_game_count_forever
    count=get_count(uid)+get_game_count_forever(uid)
    args['count']=count
    apprequset=get_apprequset(request,uid)
    request.session['apprequest']=apprequset['userUid']
    request.session['uid']=uid
    users=apprequset['users']
    args['data']=users
    args['userCount']=len(users)
    from apps.game_app.models import get_invite_confirm_list,clear_invite_confirm
    inviteNonfirmList=get_invite_confirm_list(uid)
    if not len(inviteNonfirmList)==0:
        clear_invite_confirm(uid)
    args['inviteNonfirmList']=inviteNonfirmList
    #获取匹配记录
    from apps.game_app.models import get_recommend_history
    facebookUserListDcit=get_recommend_history(uid)
    #获取在线
    friendsOnlineUid=friends_online(request)
    facebookUserRecordList=[]
    for facebookUserDcit in facebookUserListDcit:
        if  facebookUserDcit.get("uid") in friendsOnlineUid:
            facebookUserDcit['online']=1
        else:
            facebookUserDcit['online']=0
        facebookUserRecordList.append(facebookUserDcit)    
    args['facebookUserRecordList']=facebookUserRecordList
    return args
       
def debug_pintu_cache(request):   
    from django.core.cache import cache
    girls=cache.get('GIRLS')
    boys=cache.get('BOYS')
    game_forever= cache.get('USER_GAME_COUNT_FOREVE')
    invite_count=cache.get('INVITE_COUNT')
    confirm_invite=cache.get('CONFIRM_INVITE')
    from apps.common_app.models import BackupCache
    backupCaches=BackupCache.objects.all().order_by('-backupTime')
    import calendar
    backupTimes= [backupCache.backupTime.strftime('%Y-%m-%d:%H:%M:%S') for backupCache in backupCaches]
    invite_in_day=cache.get('INVITE_IN_DAY')
    return render(request,'debug_cache.html',{'girls':girls,'boys':boys,'invite_count':invite_count,'game_forever':game_forever,'confirm_invite':confirm_invite,'backupTimes':backupTimes,'invite_in_day':invite_in_day})

def debug_update(request):
    from django.core.cache import cache
    type=int(request.GET.get('type'))  
    person=simplejson.loads(request.GET.get('person'))
    pintu=request.GET.get('pintu')
    if type==1:
        type='BOYS'
    else:
        type='GIRLS'
    data=cache.get(type)
    data[pintu]= person
    cache.set(type,data)
    girls=cache.get('GIRLS')
    boys=cache.get('BOYS')
    json=simplejson.dumps({'girls':girls,'boys':boys})
    return HttpResponse(json)
 
def get_apprequset(request,uid):
    #获取好友发来的生命请求
    data=request.facebook.graph.get_object('me/apprequests',)
    users,userUid=[],[]
    for apprequest in data.get('data'):
        if apprequest.get('to').get('id')==uid and apprequest.get('application').get('id')==FaceBookAppID:
            requestId=apprequest.get('id')
            userId=apprequest.get('from').get('id')
            username=apprequest.get('from').get('name')
            from apps.game_app.models import get_invite_in_day,add_invite_in_day
            if (not userId in userUid) and userId not in get_invite_in_day(uid):
                userAvatar=FacebookUser.objects.get(uid=userId).avatar
                #添加到今天推荐过的Uid
                add_invite_in_day(uid,userId)
                userUid.append(userId)
                users.append({'uid':userId,'username':username,'avatar':userAvatar}) 
            request.facebook.graph.delete_object(requestId)
    return {'users':users,'userUid':userUid}

def facebook_save(request,uid):
        me = request.facebook.graph.get_object(uid)
        friends =request.facebook.graph.get_object(uid+'/friends').get('data')
        friendList=[]
        for friend in friends:
            friendList.append(friend.get('id'))
        friendList=simplejson.dumps(friendList)
        avatar= request.facebook.graph.get_object('me/picture',height=80,width=80)
        smallAvatar= request.facebook.graph.get_object('me/picture',height=50,width=50)
        updateTime=datetime.datetime.strptime(me.get('updated_time'),'%Y-%m-%dT%H:%M:%S+0000')
        gender=u'F'
        if me.get('gender')==u'male':
            gender='M'
        facebookUser=FacebookUser(uid=me.get('id'),username=me.get('name'),gender=gender,updateTime=updateTime,noRecommendList=friendList,link=me.get('link'))
        if 'location' in me.keys():
            facebookUser.location=me.get('location').get('name')
        if 'birthday' in me.keys():
            facebookUser.birthday=datetime.datetime.strptime(me.get('birthday'),'%m/%d/%Y')
            from datetime import date
            facebookUser.age=(date.today().year + 1)-facebookUser.birthday.year
        if not  avatar is None:
            facebookUser.avatar=avatar.get('url')
        if not smallAvatar is None:
            facebookUser.smallAvatar=smallAvatar.get('url')
        facebookUser.save()
        #保存图片
        user_photos_save(request,uid)
        
def feed(request):
     attachment={
             "link": "https://apps.facebook.com/pinloveapp/",
             'name':"fate",
             "caption": "fate",
             "description": "Find your today's fated friend on facebook",
             "picture": "http://www.pinlove.com/static/img/coin.png"}
     message='Invite friends to play the game! fate--->https://apps.facebook.com/pinloveapp/'
     authResponse=request.REQUEST.get('authResponse',False)
     if authResponse:
        authResponse=simplejson.loads(authResponse)
        from apps.third_party_login_app.facebook import GraphAPI
        graph=GraphAPI(access_token=authResponse.get('accessToken'), timeout=authResponse.get('expiresIn'))
        request.session['graph']=graph
     graph=request.session['graph']
     permissions=graph.permissions()
     if permissions.get('publish_actions',False):
         graph.put_wall_post(message,attachment)   
         json=simplejson.dumps({'result':'success'}) 
     else:
         json=simplejson.dumps({'result':'nopermission'}) 
     return HttpResponse(json)   
   
def friends_online(request):
    sql='''SELECT uid FROM user WHERE
          online_presence = 'active'
          AND uid IN (
            SELECT uid2 FROM friend where uid1 = me()
          ) '''
    friends=request.facebook.graph.fql(sql)
    friendList=[]
    for friend in friends['data']:
        friendList.append(str(friend.get('uid')))
    return friendList
         
'''
保存facebook图片
'''        
def user_photos_save(request,uid):
    albums=request.facebook.graph.get_object('me/albums')
    for album in albums.get('data'):
        photos=request.facebook.graph.get_object('%s%s' %(album.get('id'),'/photos'))
        for photo in photos.get('data') :
             id=photo.get('id')
             smailPhoto=photo.get('picture')
             bigPhoto=photo.get('source')
             if 'name' in photo.keys():
                 description=photo.get('name')
             else:
                 description=''
             FacebookPhoto(id=id,user_id=uid,smailPhoto=smailPhoto,bigPhoto=bigPhoto,description=description).save()
            
def test_get_code(request):
    from apps.third_party_login_app.facebook import auth_url
    url=auth_url('','https://apps.facebook.com/1435511770015401/',['user_location','user_birthday','user_photos'])
    data=urllib2.urlopen(url)
    return HttpResponse(data)