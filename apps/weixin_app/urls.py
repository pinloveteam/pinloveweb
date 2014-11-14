# -*- coding: utf-8 -*-
'''
Created on 2014年5月23日

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.weixin_app.views',
     url(r'^test/$', 'auth_login'),
     url(r'^/$', 'vaild'),
     
)
