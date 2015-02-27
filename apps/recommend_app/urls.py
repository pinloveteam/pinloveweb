# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.recommend_app.views',
    url(r'^user_vote/$', 'user_vote'),
    url(r'^socre_my/$', 'socre_my'),
    url(r'^get_socre_for_other/$', 'get_socre_for_other'),
   
     #更新权重                     
    url(r'^update_weight/$', 'update_weight'),
    #对另一半打分
    url(r'^grade_for_other/$', 'grade_for_other'),
    #性格标签
    url(r'^character_tags/$', 'character_tags'),
    #为对方买分
    url(r'^buy_score_for_other/$', 'buy_score_for_other'),
     #检查对另一半打分的拼爱币积分是否足够
    url(r'^check_charge_for_socre_my/$', 'check_score_and_PLprice_for_socre_my'),
    
    
)
