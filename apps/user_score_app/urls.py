# -*- coding: utf-8 -*-
'''
Created on 2014年4月5日

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.user_score_app.views',
    url(r'^$', 'user_score'),  
    url(r'^get_free_pinloveicon/$', 'get_free_pinloveicon',{'template_name':'mission.html'}),  
)

urlpatterns+=patterns('apps.user_score_app.test',
    url(r'^test/$', 'score_test'),  
)
