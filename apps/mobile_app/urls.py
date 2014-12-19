#-*- coding: UTF-8 -*- 
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.mobile_app.views',
     #账户
     url(r'^account/', 'account'),
     #获得权重
     url(r'^get_weight/$', 'get_weight'),
     
)

urlpatterns+=patterns('',
     #更新权重                     
    url(r'^update_weight/$', 'recommend_app.views.update_weight'),
    #手机充值
    url(r'^member/$', 'apps.pay_app.views.member',{'template_name':'mobile_recharge.html'}),  
    #获取免费获取拼爱币信息
    url(r'^get_free_pinloveicon/$', 'apps.user_score_app.views.get_free_pinloveicon',{'template_name':'mobile_mission.html'}),  
    #登出
    url(r'^logout/', 'pinloveweb.views.logout'),                
    url(r'^register/$','pinloveweb.views.register_user',{'template_name':'mobile_register.html','next_template_name':'mobile_recommend.html'}),
    url(r'^login/$|^$','pinloveweb.views.auth_view',{'template_name':'mobile_login.html','next_template_name':'mobile_recommend.html'}),
)
