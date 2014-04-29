# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
 #search:
urlpatterns=patterns('apps.search_app.views',
    url(r'^simple_search/$', 'simple_search'),
    url(r'^search_result/$', 'search_result'),
    url(r'^advance_search/$', 'advance_search'),
    url(r'^advance_search_result/$', 'advance_search_result'),
    url(r'^$', 'search')
)
