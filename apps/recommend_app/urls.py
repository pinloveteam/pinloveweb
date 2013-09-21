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
    #对另一半打分
    url(r'^grade_for_other/$', 'grade_for_other'),
    url(r'^user_vote/$', 'user_vote'),
    
    
)
