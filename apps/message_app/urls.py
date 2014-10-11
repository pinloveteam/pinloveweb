# -*- coding: utf-8 -*-
'''
Created on Oct 25, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns = patterns('apps.message_app.views',
    url(r'^reply/', 'message_reply'),
    url(r'^send/', 'message_send'),
    url(r'^get_no_read_messge_by_ids/$', 'get_no_read_messge_by_ids'),
    ##########
    url(r'^$','message',{'template_name': 'message_1.html'}),
    url(r'^message_list/$','message_list',{'template_name': 'message_1.html'}),
    url(r'^follow_list/$','get_follow_message',{'template_name': 'message_1.html'}),
    url(r'^detail/$', 'message_detail',{'template_name':'message_detail.html'}),
     url(r'^clean/$', 'clean'),
    url(r'^count/$', 'count'), 
    url(r'^no_read_message/$', 'no_read_message',{'template_name': 'message_1.html'}), 
     url(r'^test/$', 'message_test'),
    )
