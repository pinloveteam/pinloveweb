# -*- coding: utf-8 -*-
'''
Created on 2014年5月23日

@author: jin
'''
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
urlpatterns=patterns('apps.weixin_app.views',
     url(r'^self_info/$', 'self_info'),
     url(r'^other_info/$', 'other_info'),
     url(r'^my_character/$', 'my_character'),
     url(r'^ta_character/$', 'ta_character'),
     url(r'^score/$', 'score'),
     url(r'^share_userlist/$', 'share_userlist'),
     url(r'^compare/$', 'compare'),
     url(r'^download/$', TemplateView.as_view(template_name="weixin_download.html")),
     url(r'^test/$', 'test'),
)
