# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2013

@author: jin
'''
from django.conf.urls import patterns, url
from pinloveweb import settings
urlpatterns=patterns('apps.pay_app.views',
#     url(r'^icon/$', 'get_icon'),
#     url(r'^pay_detail/$', 'pay_detail'),
#      url(r'^pay_test/$', 'pay_test'),
#      url(r'^pay_test2/$', 'pay_test2'),
#      url(r'^pay_paypal/$', 'view_that_asks_for_money'),
#      url(r'^paypal_success/$', 'paypal_success'),
#      url(r'^paypal_cancel/$', 'paypal_cancel'),
#      url(r'^member/$', 'member'),
#      url(r'^pay_icon_order/$', 'pay_icon_order'),
#      url(r'^redeem_price/$', 'redeem_price'),
#       url(r'^charge_record/$', 'charge_record'),
#      url(r'^paypal/$', 'paypal_notify'),
     
)
if settings.DEBUG:
    urlpatterns+=patterns('apps.pay_app.test',
      url(r'^test/$', 'pay_tests'),               
)               