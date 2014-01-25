# -*- coding: utf-8 -*-
'''
Created on 2014年1月8日

@author: jin
'''
import datetime
from django.core.cache import cache
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
'''
def init_yuanfenpintu_cache():
    cache.set('ALL_PIECE',set([0,1,2,3,4,5,6,7,8,9]))
    cache.set('GAME_TIMES',10)
    cache.set('NO_MATCHING_USER',"0")
    cache.set('GAME_TIMES_REACH_THE_LIMIT',"1")
    cache.set('MATCH_SUCCESS',"2")
    cache.set('TODAY',datetime.date.today())
    cache.set('GIRLS',{})
    cache.set('BOYS',{})
    cache.set('USER_GAME_COUNT',{})

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
        

