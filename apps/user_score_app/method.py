# -*- coding: utf-8 -*-
'''
Created on 2014年4月5日

@author: jin
'''
from apps.user_app.models import UserProfile
from apps.user_score_app.models import UserScoreExchangeRelate, UserScore,\
    UserScoreDtail
from django.db import transaction
from django.core.cache import cache
from apps.user_score_app.user_score_settings import DAY_INIVITE_FRIEND_COUNT
'''
 邀请好友注册奖励
'''

def get_score_by_invite_friend_register(inviteCode):
    try:
        if UserProfile.objects.filter(link=inviteCode).exists():
            userProfile=UserProfile.objects.get(link=inviteCode)
            user_score_save(userProfile.user_id,'1002')
            return True
        else:
            return False
    except AssertionError as e:
        return False
'''
用户登录
'''
def get_score_by_user_login(userId):
    count=get_day_login_count(userId)
    if count<DAY_INIVITE_FRIEND_COUNT:
        user_score_save(userId,'1001')
        set_day_login_count(userId,count+1)
    return True

'''
邀请好友登录
'''
def get_score_by_invite_friend_login(inviteCode,userId):
    try:
        if UserProfile.objects.filter(link=inviteCode).exclude(user_id=userId).exists():
            userProfile=UserProfile.objects.get(link=inviteCode)
            count=get_invite_friend_count(userProfile.user_id)
            if count<DAY_INIVITE_FRIEND_COUNT:
                user_score_save(userProfile.user_id,'1003')
                set_invite_friend_count(userProfile.user_id,count+1)
            return True
        else:
            return False
    except AssertionError as e:
        return False  

'''
保存积分
'''
@transaction.commit_on_success    
def user_score_save(userId,type):
    userScoreExchangeRelate=UserScoreExchangeRelate.objects.get(type=type)
    userScore=UserScore.objects.get(user_id=userId)
    userScore.validScore+=userScoreExchangeRelate.amount
    userScore.save()
    UserScoreDtail(userScore=userScore,exchangeRelate_id=userScoreExchangeRelate.id,amount=userScoreExchangeRelate.amount).save()

'''
获取用户登录积分缓存
'''
def set_invite_friend_count(uid,count):
    invite_count = cache.get('DAY_INIVITE_FRIEND_COUNT')
    invite_count[uid]=count
    cache.set('DAY_INIVITE_FRIEND_COUNT',invite_count)
    
def get_invite_friend_count(uid):
    user_game_count_forever = cache.get('DAY_INIVITE_FRIEND_COUNT')
    if user_game_count_forever.get(uid) == None :
        user_game_count_forever[uid] = 0
        cache.set('DAY_INIVITE_FRIEND_COUNT',user_game_count_forever)
    return cache.get('DAY_INIVITE_FRIEND_COUNT').get(uid)

def set_day_login_count(uid,count):
    invite_count = cache.get('DAY_LOGIN_COUNT')
    invite_count[uid]=count
    cache.set('DAY_LOGIN_COUNT',invite_count)
    
def get_day_login_count(uid):
    user_game_count_forever = cache.get('DAY_LOGIN_COUNT')
    if user_game_count_forever.get(uid) == None :
        user_game_count_forever[uid] = 0
        cache.set('DAY_LOGIN_COUNT',user_game_count_forever)
    return cache.get('DAY_LOGIN_COUNT').get(uid)
        
