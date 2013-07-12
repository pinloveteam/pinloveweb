from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.user_app.views',
    url(r'^update_profile/$', 'update_profile'), 
    url(r'^update_profile_success/$', 'update_profile_success'), 
    url(r'^userInfor/(.+)/$', 'userInfor'),
     url(r'^addFriend/$', 'addFriend'),
)
 #search:
urlpatterns+=patterns('apps.user_app.views',
    url(r'^simple_search/$', 'simple_search'),
    url(r'^search_result/$', 'search_result'),
)
