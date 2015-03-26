# -*- coding: utf-8 -*-
'''
Created on 2014年1月8日

@author: jin
'''
import datetime
from django.core.cache import cache
from django.utils import simplejson
'''
初始化缓存
'''
def init_cache():
    init_game_cache()
    init_tag()
    init_recommend()
    init_user_score()

'''
在登录是初始化cache信息
'''
def init_info_in_login(userId):
    info={}
    if len(get_profile_cache(userId))>0:
        del_profile_cache(userId)
    #初始化黑名单
    from apps.user_app.method import get_black_list
    BACKLIST=get_black_list(userId)
    info['BACKLIST']=BACKLIST
    #初始化不推荐用户
    from apps.recommend_app.method import get_no_recommend_list
    info['NORECOMMENDLIST']=get_no_recommend_list(userId)
    set_profile_cache(userId,info)

'''
在登出是删除cache信息
'''  
def del_cache_in_logout(userId):
    if len(get_profile_cache(userId))>0:
        del_profile_cache(userId)
'''
初始化游戏缓存
'''
def init_game_cache():
    init_yuanfenpintu_cache()
    
'''
初始化缘分拼图缓存
INVITE_IN_DAY  一天中邀请过的人
'''
def init_yuanfenpintu_cache():
    cache.set('ALL_PIECE',set([0,1,2,3,4,5,6,7,8,9]))
    cache.set('GAME_TIMES',10)
    cache.set('NO_MATCHING_USER',"0")
    cache.set('GAME_TIMES_REACH_THE_LIMIT',"1")
    cache.set('MATCH_SUCCESS',"2")
    cache.set('TODAY',datetime.date.today())
    NAMES=['GIRLS','BOYS','USER_GAME_COUNT','USER_GAME_COUNT_FOREVE','INVITE_COUNT','CONFIRM_INVITE','INVITE_IN_DAY']
    WEB_NAMES=['WEB_GIRLS','WEB_BOYS']
    NAMES.extend(WEB_NAMES)
    for name in NAMES:
        if cache.get(name)==None:
            cache.set(name,{})
#     if cache.get('GIRLS')==None:
#         cache.set('GIRLS',{})
#     if cache.get('BOYS')==None:
#         cache.set('BOYS',{})
#     if cache.get('USER_GAME_COUNT')==None:
#         cache.set('USER_GAME_COUNT',{})
#     if cache.get('USER_GAME_COUNT')==None:
#         cache.set('USER_GAME_COUNT_FOREVE',{})
#     cache.set('INVITE_COUNT',{})
    cache.set('INVITE_TIME_A_LIFE',3)

'''
初始化推荐
HAS_RECOMMEND 是否需要做实时推荐
'''
def init_recommend():
    NAMES=['HAS_RECOMMEND',]
    for name in NAMES:
        if cache.get(name)==None:
            cache.set(name,{})
 
'''
初始化用户积分
 DAY_LOGIN_COUNT每天登入次数,小于5次给积分
 DAY_INIVITE_FRIEND_COUNT 邀请好友登录次数
'''           
def init_user_score():
    NAMES=['DAY_INIVITE_FRIEND_COUNT','DAY_LOGIN_COUNT']
    for name in NAMES:
        if cache.get(name)==None:
            cache.set(name,{})

'''
 获得各个数据表的推荐所需的数据完成情况
 如全部完成则返回true
'''           
def get_has_recommend(user_id):
    recommend=cache.get('HAS_RECOMMEND')
    fieldList=['userExpect','weight','tag','info',"avatar"]
    if recommend.get(user_id)==None:
        recommend[user_id]=dict((field,False) for field in fieldList)
        return False
    else:
        user=recommend.get(user_id)
        for field in fieldList:
            if user.get(field,False)==False:
                return False
        return True

'''
获取推荐数据填写状态
'''
def get_recommend_status(user_id):
    recommend=cache.get('HAS_RECOMMEND')
    if recommend.get(user_id)==None:
        fieldList=['userExpect','weight','tag','info',"avatar"]
        recommend[user_id]=dict((field,False) for field in fieldList)
    user=recommend.get(user_id)
    return user
    
'''
用于判断各个数据表的推荐所需的数据是否填写完成
'''
def has_recommend(user_id,field):
    recommend=cache.get('HAS_RECOMMEND')
    flag,fieldList=False,['userExpect','weight','tag','info',"avatar"]
    if field not in fieldList:
        return None
    if recommend.get(user_id)==None:
        recommend[user_id]=dict((field,False) for field in fieldList)
    user=recommend.get(user_id)
    if field =='userExpect':
        from apps.recommend_app.models import UserExpect
        if UserExpect.objects.filter(user_id=user_id).exists() and (not (UserExpect.objects.filter(user_id=user_id ,heighty1=0.00,heighty2=0.00,heighty3=0.00,heighty4=0.00,heighty5=0.00,heighty6=0.00,heighty7=0.00,heighty8=0.00).exists())):
            flag=True
    elif field =='weight':
        from apps.recommend_app.models import Grade
        if Grade.objects.filter(user_id=user_id,heightweight__isnull=False,incomeweight__isnull=False,educationweight__isnull=False,appearanceweight__isnull=False).exists():
            flag=True
    elif field=='tag':
        from apps.user_app.models import UserTag
        if UserTag.objects.filter(user_id=user_id,type=1).exists() and UserTag.objects.filter(user_id=user_id,type=0).exists():
            flag=True
    elif field == 'avatar':
        from apps.user_app.models import UserProfile
        if UserProfile.objects.filter(user_id=user_id,avatar_name_status__in=[u'2',u'3']):
            flag=True
    elif field=='info':
        from apps.user_app.models import UserProfile
        if UserProfile.objects.filter(user_id=user_id,income__gt=-1,education__gt=-1,height__gt=-1).exclude(educationSchool=None).exists():
            flag=True
    user[field]=flag
    recommend[user_id]=user
    cache.set('HAS_RECOMMEND',recommend)
'''
 用户标签
'''
def init_tag():
    from apps.common_app.models import Tag
    try:
        tags=Tag.objects.filter()
    except Exception as e:
        print e
    tagList=[]
    tagList1=[]
    i=0
    for tag in tags:
        tagList1.append((tag.id,tag.content))
        i+=1
        if i>=3:
            tagList.append(tagList1)
            tagList1=[]
            i=0
    cache.set('TAG',tuple(tagList))
'''
插入可以值，如果值为None，则创建
'''
def set_cache(key,value):
    data=cache.get(key)
    #如果 args 不为空
    if data is None:
        cache.set(key,[value,])
    else:
        data.append(value)
        cache.set(key,data)
    
'''
获取用户个人的cache信息
@param userId:  用户id
'''
def get_profile_cache(userId):
    return cache.get('%s%s'%('pinlove_',userId),{})

'''
修改用户个人的cache信息
@param userId:  用户id
@param info: 用户cache信息
'''
def set_profile_cache(userId,info):
    cache.set('%s%s'%('pinlove_',userId),info)

'''
删除用户个人的cache信息
@param userId:  用户id
'''  
def del_profile_cache(userId,):
    cache.delete('%s%s'%('pinlove_',userId))
'''
备份缓存数据  
backupType： 备份数据类型
      PINTU  拼图游戏备份
'''
def backup_cache(backupType):
    from apps.common_app.models import BackupCache
    import util_settings
    menthods=getattr(util_settings, backupType)
    backupCache=BackupCache()
    for menthod in menthods:
        data=simplejson.dumps(cache.get('menthod'))
        getattr(backupCache,menthod,data)
    backupCache.save()
'''
'''
def restore_backup_cache(backupType,time):
    from apps.common_app.models import BackupCache
    sql="select * from backup_cache where backupTime='"+str(time)+"'"
    backupCache=BackupCache.objects.raw(sql)[0]
    import util_settings
    menthods=getattr(util_settings, backupType)
    for menthod in menthods:
        data=getattr(backupCache,menthod)
        cache.set(menthod,simplejson.loads(data))

###########黑名单################
'''
获得黑名单列表
@return: list 黑名单列表
'''
def get_black_list_by_cache(myId):
    profile=get_profile_cache(myId)
    blackList=profile.get('BACKLIST',[])
    return  blackList
'''
将用户id缴入黑名单列表
'''
def set_black_list_by_cache(myId,userId):
    myId=int(myId)
    userId=int(userId)
    profile=get_profile_cache(myId)
    blackList=profile.get('BACKLIST',[])
    blackList.append(userId)
    profile['BACKLIST']=blackList
    set_profile_cache(myId,profile)
    
def is_black_list(myId,userId):
    profile=get_profile_cache(myId)
    blackList=profile.get('BACKLIST',[])
    if userId in blackList:
        return True
    else:
        return False
'''
删除黑名单列表
@return: list 黑名单列表
'''
def del_attribute_black_list_by_cache(myId,userId):
    profile=get_profile_cache(myId)
    blackList=profile.get('BACKLIST',[])
    blackList.remove(userId)
    profile['BACKLIST']=blackList
    set_profile_cache(myId,profile)
    ###########黑名单################
    
    
    ############不推荐用户###############
'''
获得不推荐用户列表
@return: list 不推荐用户列表
'''
def get_no_recomend_list_by_cache(myId):
    profile=get_profile_cache(myId)
    blackList=profile.get('NORECOMMENDLIST',[])
    return  blackList
'''
将用户id加入不推荐用户列表
'''
def set_no_recomend_list_by_cache(myId,userId):
    myId=int(myId)
    userId=int(userId)
    profile=get_profile_cache(myId)
    blackList=profile.get('NORECOMMENDLIST',[])
    blackList.append(userId)
    profile['NORECOMMENDLIST']=blackList
    set_profile_cache(myId,profile)
    
'''
删除不推荐用户
@return: list 不推荐用户列表
'''
def del_no_recomend_list_by_cache(myId,userId):
    profile=get_profile_cache(myId)
    blackList=profile.get('NORECOMMENDLIST',[])
    blackList.remove(userId)
    profile['NORECOMMENDLIST']=blackList
    set_profile_cache(myId,profile)
    ############不推荐用户###############