# -*- coding: utf-8 -*-
'''
Created on Oct 25, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns = patterns('apps.message_app.views',
    url(r'^list/$', 'list'), 
    url(r'^delete_notify/', 'delete_notify'), 
    
    url(r'^reply/', 'message_reply'),
    url(r'^send/', 'message_send'),
    url(r'^has_new_message/$', 'has_new_message'),
    url(r'^get_messge_by_id/$', 'get_messge_by_id'),
    url(r'^get_noread_messges/$','get_noread_messges_by_userid'),
    ##########
    url(r'^$','message',{'template_name': 'message_1.html'}),
     url(r'^detail/$', 'message_detail'),
     url(r'^clean/$', 'clean'),
    url(r'^count/$', 'count'), 
    url(r'^no_read_message/$', 'no_read_message',{'template_name': 'message_1.html'}), 
     url(r'^test/$', 'message_test'),
    )
