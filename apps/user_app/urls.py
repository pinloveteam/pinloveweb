# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.user_app.views',
    url(r'^user_profile/$', 'user_profile'), 
    url(r'^update_profile/$', 'update_profile'),       
    url(r'^update_basic_profile/$', 'update_Basic_Profile_view'), 
    url(r'^contact/$', 'user_contact_view'), 
    url(r'^appearance/$', 'user_appearance_view'), 
    url(r'^study_work/$', 'user_study_work_view'), 
#     url(r'^hobby_interest/$', 'hobby_interest_view'), 
    url(r'^personal_habit/$', 'personal_habit_view'), 
    url(r'^family_information/$', 'family_information_view'), 
    url(r'^update_profile_success/$', 'update_profile_success'), 
    url(r'^userInfor/(.+)/$', 'userInfor'),
     url(r'^update_follow/$', 'update_follow'),
     url(r'^change_password/$', 'change_password',{'tempate_name':'member/change_password.html'}),
     url(r'^friend/$', 'friend'),
     url(r'^removeFriend/(.+)/$', 'removeFriend'),
     url(r'^reset_password/$', 'reset_password'),
     url(r'^commit_password/$', 'commit_password'),
     #url(r'^alter_password/$', 'alter_password'),
     url(r'^upload/$', 'upload'),
     url(r'^photo_check/$', 'photo_check'),
     #关注
     url(r'^follow/(.+)/$', 'follow'),
     #详细信息
     url(r'^detailed_info/$', 'detailed_info'),
     #不喜欢
     url(r'^dislike/$', 'dislike'),
     url(r'^member/$','member'),
     url(r'^become_member/$','become_member'),
     url(r'^cancel_member/$','cancel_member'),
     
    )
#1.0使用
urlpatterns += patterns('apps.user_app.views',
    
)