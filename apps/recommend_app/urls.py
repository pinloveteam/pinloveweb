# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.recommend_app.views',
    url(r'^recommend/?page', 'recommend'),
    url(r'^recommend/$', 'recommend'),
    #权重
    url(r'^weight/$', 'weight'),
    url(r'^user_vote/$', 'user_vote'),
    url(r'^socre_my/$', 'socre_my'),
    url(r'^get_socre_for_other/$', 'get_socre_for_other'),
    url(r'^test_match/$', 'test_match'),
    
)
urlpatterns+=patterns('apps.recommend_app.views',
    #更新权重                     
    url(r'^update_weight/$', 'update_weight'),
    #对另一半打分
    url(r'^grade_for_other/$', 'grade_for_other'),
    #性格标签
    url(r'^character_tags/$', 'character_tags'),
)                 
