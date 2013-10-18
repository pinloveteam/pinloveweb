# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.publish_app.views',
    url(r'^list/$', 'list'),
    url(r'^(\d+)/$', 'publish'),
    url(r'^upload_image/', 'upload_image'),
     url(r'^test/', 'test'),
    
)
