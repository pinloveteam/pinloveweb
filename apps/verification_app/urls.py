# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
 #search:
urlpatterns=patterns('apps.verification_app.views',
    url(r'^list/$', 'verif_list'),
    #email valid
    url(r'^emailvalid/$', 'emailvalid'),
    url(r'^emailValidConfirm/$', 'emailvalid_confirm'),
    #IDCardValid valid
    url(r'^IDCardValid/$', 'IDcard_valid'),
    #educationValid valid
    url(r'^educationValid/$', 'education_valid'),
    #incomeValid valid
    url(r'^incomeValid/$', 'income_valid'),
    url(r'^11/$', 'income_valid'),
    
    
)
