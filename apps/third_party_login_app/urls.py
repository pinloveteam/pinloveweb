# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url, static

#user
urlpatterns = patterns('apps.third_party_login_app.views',
    #sqq login_url
    url(r'^qq_login_url/', 'get_qq_login_url'),
    url(r'^qq_login/', 'qq_login'),
    
    #sina login_url
    url(r'^sina_login_url/', 'sina_login_url'),
    url(r'^sina_login/', 'sina_login'),
    
    #login in facebook url
    url(r'^facebook_login_url/', 'facebook_login_url'),
    url(r'^facebook_login/', 'facebook_login'),
    
    url(r'^facebook_friend_list/', 'get_facebook_friend_list'),
    url(r'^facebook_feeds/', 'facebook_feeds'),
    
    #login in twitter url
    url(r'^twitter_login_url/', 'twitter_login_url'),
    url(r'^twitter_login/', 'twitter_login'),
    url(r'^update_gender/$','update_gender')
    
    
)


