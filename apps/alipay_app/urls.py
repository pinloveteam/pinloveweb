# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2013

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.alipay_app.views',
                     url(r'^/$', 'dpn', {'item_check_callable':None}, name='alipay-dpn'),
                     url(r'^/paid/$', 'paid', {'template_name':'alipay_paid.html'},),
                     
)
