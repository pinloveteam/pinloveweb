# -*- coding: utf-8 -*-
'''
Created on 2014年4月5日

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.user_score_app.views',
    url(r'^test/$', 'score_test1'), 
    url(r'^$', 'user_score'),  
    
)