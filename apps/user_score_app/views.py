# -*- coding: utf-8 -*-
'''
Created on 2014年4月5日

@author: jin
'''
from apps.user_app.models import UserProfile, UserVerification
from apps.user_score_app.models import UserScore, UserScoreDtail
from django.shortcuts import render
from django.http.response import HttpResponse

def user_score(request):
    arg={}
    userProfile=UserProfile.objects.get(user=request.user)
    arg['link']=userProfile.link
    userScore=UserScore.objects.get(user_id=request.user.id)
    arg['userScore']=userScore
    userScoreDtail=UserScoreDtail.objects.filter(userScore=userScore)
    arg['userScoreDtail']=userScoreDtail
    from apps.user_score_app.method import get_invite_friend_count,get_day_login_count
    arg['dayLoginCount']=get_day_login_count(request.user.id)
    arg['inviteFriendLogin']=get_invite_friend_count(request.user.id)
    return render(request,'user_score.html',arg)


def score_test(request):
    num=request.GET.get('num',False)
    from apps.user_score_app.method import get_score_by_invite_friend_register,get_score_by_user_login
    get_score_by_invite_friend_register(num)
    get_score_by_user_login(request.user.id)
    from apps.user_score_app.method import get_score_by_invite_friend_login
    get_score_by_invite_friend_login(num)
    return HttpResponse('succes')
    
def score_test1(request):
    userProfileList=UserProfile.objects.all()
    for userProfile in userProfileList:
      if userProfile.link=='me':
        from pinloveweb.method import create_invite_code
        userProfile.link=create_invite_code(userProfile.user_id)
        userProfile.save()
#     userScoreList=UserScore.objects.all()
#     from django.contrib.auth.models import User
#     userList=User.objects.all()
#     idList=[]
#     idLists=[]
#     for userScore in userScoreList:
#         idList.append(userScore.user_id)
#     for user in userList:
#         if not user.id in idList:
#             idLists.append(user.id)
#     userScoreList=[]
#     for id in idLists:
#         userScore=UserScore()
#         userScore.user_id=id
#         userScoreList.append(userScore)
#     UserScore.objects.bulk_create(userScoreList)
    return HttpResponse('succes')

'''
免费获取拼爱币页面
'''
def get_free_pinloveicon(request,template_name):
    args={}
    try:
        userProfile=UserProfile.objects.get(user=request.user)
        args['link']=userProfile.link
        from apps.user_score_app.method import get_day_login_count
        #获取每日登陆
        args['dayLoginCount']=get_day_login_count(request.user.id)
        from apps.user_score_app.user_score_settings import DAY_INIVITE_FRIEND_COUNT,DAY_LOGIN_COUNT
        args['DAY_INIVITE_FRIEND_COUNT']=DAY_INIVITE_FRIEND_COUNT
        #获取邀请登录时间
        args['DAY_LOGIN_COUNT']=DAY_LOGIN_COUNT
        from apps.user_score_app.method import get_invite_friend_count
        args['inviteFriendLogin']=get_invite_friend_count(request.user.id)
        #认证
        userVerification=UserVerification.objects.get(user_id=request.user.id)
        args['avatar_name_status']=userProfile.avatar_name_status
        for field in ['incomeValid','educationValid']:
            args[field]=getattr(userVerification,field)
            
        
        args['userProfileFinish']=False
        fields = ( 'income','weight','jobIndustry',
        'height', 'education', 'day_of_birth','educationSchool','city')
        for field in fields:
            if  not getattr(userProfile,field) in [-1,'N',None,u'',u'地级市、县',u'国家',u'请选择']:
                args['userProfileFinish']=True
        return render(request,template_name,args)
    except  Exception as e:
        args={'error_message':e.message}
        return render(request,'error.html',args)
    