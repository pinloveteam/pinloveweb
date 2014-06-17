# -*-coding: utf-8 -*-
'''
Created on Nov 5, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns = patterns('apps.friend_dynamic_app.views',
     url(r'^send/$', 'send_dynamic'),
     url(r'^person/$', 'person_dynamic'),
     url(r'^updatePhoto/$', 'update_photo'),
     url(r'^deletePhoto/$','delete_photo'),
     url(r'^updateVideo/$', 'update_video'),
     url(r'^delDynamic/$', 'del_dynamic'),
     url(r'^agree/$', 'agree'),
     url(r'^show_comment/$', 'show_comment'),
     url(r'^comment/$', 'comment'),
     url(r'^del_comment/$', 'del_comment'),
      url(r'^$', 'dynamic'), 
)