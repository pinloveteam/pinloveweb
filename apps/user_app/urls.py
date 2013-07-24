from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.user_app.views',
     url(r'^update_profile/$', 'update_profile'), 
     url(r'^update_profile_success/$', 'update_profile_success'), 
     url(r'^userInfor/(.+)/$', 'userInfor'),
     url(r'^addFriend/$', 'addFriend'),
     url(r'^friend/$', 'friend'),
     url(r'^removeFriend/(.+)/$', 'removeFriend'),
     
     url(r'^forget_password/$', 'forget_password'),
     url(r'^reset_password/$', 'reset_password'),
     url(r'^commit_password/$', 'commit_password'),
     url(r'^alter_password/$', 'alter_password'),
)
 #search:
urlpatterns+=patterns('apps.user_app.views',
    url(r'^simple_search/$', 'simple_search'),
    url(r'^search_result/$', 'search_result'),
)
