# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.pay_app.views',
    url(r'^icon/$', 'get_icon'),
    url(r'^pay/$', 'pay'),
    
)
