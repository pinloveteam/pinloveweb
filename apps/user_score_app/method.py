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
被查看分数获得积分
'''
def get_score_by_viewed_score(userId):
    user_score_save(userId,1009)
    return True

def get_score_by_avatar_check(userId):
    '''
    头像认证通过
    '''
    user_score_save(userId,1005)
    return True
    
def get_score_by_verification(userId,verificationType):
    '''
    获得积分通过认证
    attridute:
     userId 用户id
     verificationType 认证类型['education_verification','income_verification','IDCard_verification']
     '''
    
    from apps.user_score_app.user_score_settings import VERIFICATION_SCORE
    verificationData=VERIFICATION_SCORE.get(verificationType,False)
    if verificationData:
        user_score_save(userId,1006,data=verificationData)
        return True
 

def get_score_by_finish_proflie(userId,proflieTypeList):
    '''
    获得积分通过完成个人信息
    attridute:
     userId 用户id
     proflieTypeList 个人信息类型列表
     '''
    from apps.user_score_app.user_score_settings import PROFILE_SCORE
    for proflieType in proflieTypeList:
        proflieData=PROFILE_SCORE.get(proflieType,False)
        if type:
            user_score_save(userId,'1004',data=proflieData)
            
'''
消耗积分查看对象分数
attridute:
     userId 查看用户id
     otherUserId 被查看用户id
return：
   'less'  积分不足
    'success' 成功
'''
def use_score_by_other_score(userId,otherUserId):
    result=user_score_save(userId,'1008')
    if result=='success':
        get_score_by_viewed_score(otherUserId)
    return result
        
        
            
'''
保存积分
attridute:
    userId 用户id
    type   积分操作类型
    **kwargs：data(option)  说明
return:
    less 消耗积分超过剩余有效积分
    success 积分修改成功
'''
@transaction.commit_on_success    
def user_score_save(userId,type,*args,**kwargs):
    userScoreExchangeRelate=UserScoreExchangeRelate.objects.get(type=type)
    userScore=UserScore.objects.get(user_id=userId)
    if userScoreExchangeRelate.amount+userScore.validScore<0:
        return 'less'
    userScore.validScore+=userScoreExchangeRelate.amount
    userScore.save()
    data=kwargs.get('data',False)
    if not data:
        data=userScoreExchangeRelate.instruction
    UserScoreDtail(userScore=userScore,exchangeRelate_id=userScoreExchangeRelate.id,amount=userScoreExchangeRelate.amount,data=data).save()
    return 'success'



def user_score_freeze(userId,type,amount,data,*args,**kwargs):
    '''
冻结积分
'''
    userScore=UserScore.objects.get(user_id=userId)
    userScore.validScore-=amount
    userScore.freezeScore+=amount
    userScore.save()
    UserScoreDtail(userScore=userScore,exchangeRelate_id='1107',amount=amount,data=data).save()
    
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
        
def reset_count():
    '''
      重置积分变量
    '''
    cache.set('DAY_LOGIN_COUNT',{})
    cache.set('DAY_INIVITE_FRIEND_COUNT',{})