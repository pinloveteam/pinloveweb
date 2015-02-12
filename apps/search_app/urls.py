# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
 #search:
urlpatterns=patterns('apps.search_app.views',
    url(r'^$', 'search')
)
