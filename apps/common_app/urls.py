#-*- coding: UTF-8 -*- 
'''
Created on 2014年12月23日

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.common_app.views',
     #查询学校
     url(r'^select_school/', 'select_school'),
)
