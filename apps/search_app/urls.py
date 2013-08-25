from django.conf.urls import patterns, include, url
 #search:
urlpatterns=patterns('apps.search_app.views',
    url(r'^simple_search/$', 'simple_search'),
    url(r'^search_result/$', 'search_result'),
)
