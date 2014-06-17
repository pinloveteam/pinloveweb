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
    int_user_score()

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
def int_user_score():
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
    if recommend.get(user_id)==None:
        recommend[user_id]={'userProfile':False,'userExpect':False,'grade':False,'tag':False}
        return False
    else:
         user=recommend.get(user_id)
         if user.get('userProfile') and user.get('userExpect') and user.get('grade') and user.get('tag'):
             return True
         else:
             return False

'''
获取推荐数据填写状态
'''
def get_recommend_status(user_id):
    recommend=cache.get('HAS_RECOMMEND')
    if recommend.get(user_id)==None:
        recommend[user_id]={'userProfile':False,'userExpect':False,'grade':False,'tag':False}
    user=recommend.get(user_id)
    return user
    
'''
用于判断各个数据表的推荐所需的数据是否填写完成
'''
def has_recommend(user_id,field):
    recommend=cache.get('HAS_RECOMMEND')
    if recommend.get(user_id)==None:
        recommend[user_id]={'userProfile':False,'userExpect':False,'grade':False,'tag':False}
    user=recommend.get(user_id)
    if field =='userProfile':
        from apps.user_app.models import UserProfile
        from django.db.models.query_utils import Q
        if UserProfile.objects.filter(user_id=user_id).filter(height__gt=-1,avatar_name_status=3,income__gt=-1).filter(Q(education__gt=-1)|Q(educationSchool__isnull=False)).exists():
            user['userProfile']=True
    elif field =='userExpect':
        from apps.recommend_app.models import UserExpect
        if not (UserExpect.objects.filter(user_id=user_id ,heighty1=0.00,heighty2=0.00,heighty3=0.00,heighty4=0.00,heighty5=0.00,heighty6=0.00,heighty7=0.00,heighty8=0.00).exists()):
            user['userExpect']=True
    elif field =='grade':
        from apps.recommend_app.models import Grade
        if Grade.objects.filter(user_id=user_id,heightweight__isnull=False,incomescore__isnull=False,incomeweight__isnull=False,educationscore__isnull=False,educationweight__isnull=False,appearancescore__isnull=False,appearanceweight__isnull=False).exists():
            user['grade']=True
    elif field=='tag':
        from apps.user_app.models import UserTag
        if UserTag.objects.filter(user_id=user_id,type=1).exists() and UserTag.objects.filter(user_id=user_id,type=0).exists():
            user['tag']=True
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


