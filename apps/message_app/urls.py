# -*- coding: utf-8 -*-
'''
Created on Oct 25, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns = patterns('apps.message_app.views',
    url(r'^count/$', 'count'), 
    url(r'^list/$', 'list'), 
    url(r'^delete_notify/', 'delete_notify'), 
    url(r'^notify_detail/(.+)', 'notify_detail'),
    url(r'^detail/(.+)', 'message_detail'),
    url(r'^reply/', 'message_reply'),
    url(r'^send/', 'message_send'),
    url(r'^has_new_message/$', 'has_new_message'),
    
    )
