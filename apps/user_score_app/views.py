# -*- coding: utf-8 -*-
'''
Created on 2014年4月5日

@author: jin
'''
from apps.user_app.models import UserProfile
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
    