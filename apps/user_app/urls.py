from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.user_app.views',
    url(r'^update_basic_profile/$', 'update_Basic_Profile_view'), 
    url(r'^contact/$', 'user_contact_view'), 
    url(r'^appearance/$', 'user_appearance_view'), 
    url(r'^study_work/$', 'user_study_work_view'), 
#     url(r'^hobby_interest/$', 'hobby_interest_view'), 
    url(r'^personal_habit/$', 'personal_habit_view'), 
    url(r'^family_information/$', 'family_information_view'), 
    url(r'^update_profile_success/$', 'update_profile_success'), 
    url(r'^userInfor/(.+)/$', 'userInfor'),
     url(r'^addFriend/$', 'addFriend'),
     url(r'^change_password/$', 'change_password'),
     url(r'^friend/$', 'friend'),
     url(r'^removeFriend/(.+)/$', 'removeFriend'),
     url(r'^forget_password/$', 'forget_password'),
     url(r'^reset_password/$', 'reset_password'),
     url(r'^commit_password/$', 'commit_password'),
     url(r'^alter_password/$', 'alter_password'),
     url(r'^upload/$', 'upload'),
)
 #search:
urlpatterns+=patterns('apps.user_app.views',
    url(r'^simple_search/$', 'simple_search'),
    url(r'^search_result/$', 'search_result'),
)
