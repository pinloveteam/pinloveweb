#-*- coding: UTF-8 -*- 
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.mobile_app.views',
     #账户
     url(r'^account/', 'account'),
     #获得权重
     url(r'^get_weight/$', 'get_weight'),
     #推荐页面
     url(r'^loggedin/', 'recommend',),
     #个人信息页面
     url(r'^profile/', 'profile',),
     #标签页面
     url(r'^character_tag/', 'character_tag',),
     #拼爱拼图
     url(r'^pintu/', 'pintu',),
     #推荐页面
     url(r'^nearby/', 'nearby',),
     #个人信息
     url(r'^info_detail/(\d)/$','info_detail'),
     #用户外貌打分
     url(r'^vote/$','user_vote'),
     #编辑面板
     url(r'^editer/$','editer'),
     #搜索
     url(r'^search/$','search')
     
     
     
)

urlpatterns+=patterns('',
     #更新权重                     
    url(r'^update_weight/$', 'recommend_app.views.update_weight'),
    #手机充值
    url(r'^member/$', 'apps.pay_app.views.member',{'template_name':'mobile_recharge.html'}),  
    #获取免费获取拼爱币信息
    url(r'^get_free_pinloveicon/$', 'apps.user_score_app.views.get_free_pinloveicon',{'template_name':'mobile_mission.html'}),  
     url(r'^loggedin/', 'pinloveweb.views.loggedin',{'template_name':'mobile_recommend.html'}),
    #登出
    url(r'^logout/', 'pinloveweb.views.logout'),                
    url(r'^register/$','pinloveweb.views.register_user',{'template_name':'mobile_register.html'}),
    url(r'^auth/$','pinloveweb.views.auth_view',{'template_name':'mobile_login.html'}),
    url(r'^$','pinloveweb.views.login',{'template_name':'mobile_login.html','nextUrl':'loggedin'})
)
