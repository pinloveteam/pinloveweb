# -*-coding: utf-8 -*-
'''
Created on Nov 5, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns = patterns('apps.friend_dynamic_app.views',
     url(r'^send/$', 'send_dynamic'),
     url(r'^updatePhoto/$', 'update_photo'),
     url(r'^updateVideo/$', 'update_video'),
)