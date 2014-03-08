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
