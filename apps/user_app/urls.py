from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^update_profile/$', 'apps.user_app.views.update_profile'), 
    url(r'^update_profile_success/$', 'apps.user_app.views.update_profile_success'), 
)
 #search:
urlpatterns+=patterns('apps.user_app.views',
    url(r'^simple_search/', 'simple_search'),
    url(r'^search_result/', 'search_result'),
)
