#-*- coding: UTF-8 -*- 
from django.conf.urls import patterns, url
from apps.third_party_login_app.setting import QQ_MOBILE_CALLBACK_URL,\
    SINA_MOBILE_CALLBACK_URL, FACEBOOK_MOBILE_CALLBACK_URL,\
    WEIXIN_MOBILE_CALLBACK_URL
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
     url(r'^info_detail/(\d+)/$','info_detail'),
     #用户外貌打分
#      url(r'^vote/$','user_vote'),
     #编辑面板
     url(r'^editer/$','editer'),
     #搜索
     url(r'^search/$','search'),
     #雷达图
     url(r'^radar/(\d+)/$','radar'),
     url(r'^radar_compare/$','update_radar_compare'),
     #上传头像
      url(r'^update_avtar/$','update_avtar'),
       #身高打分
      url(r'^grade_height/$','grade_height'),
      #关注，粉丝
      url(r'^follow/(\d+)/$','follow'),
      
        #认证
    url(r'^verification/$','verification'),
     
)

urlpatterns+=patterns('',
     
       #上传头像
    url(r'^uploadavatar_upload/$','apps.upload_avatar.views.upload_avatar'),
    #动态
     url(r'^dynamic/$', 'apps.friend_dynamic_app.views.dynamic',{'template_name':'mobile_trend.html'}), 
   #修改密码
    url(r'^change_password/$', 'apps.user_app.views.change_password',{'tempate_name':'mobile_change_password.html'}),
     #退出
     url(r'^logout/$', 'pinloveweb.views.logout',{'redirect':'/mobile/'}),
    #忘记密码
    url(r'^forget_password/$', 'pinloveweb.views.forget_password',{'template_name':'mobile_forget_password.html'}),
    
    #个人动态
    url(r'^dynamic_person/$','apps.friend_dynamic_app.views.person_dynamic',{'template_name':'mobile_trend.html'}), 
    
    #手机qq登陆
     url(r'^qq_login_url/$', 'apps.third_party_login_app.views.get_qq_login_url',{'CALLBACK_URL':QQ_MOBILE_CALLBACK_URL}),
     url(r'^qq_login/$', 'apps.third_party_login_app.views.qq_login',{'CALLBACK_URL':QQ_MOBILE_CALLBACK_URL}),
    #手机微博登陆
     url(r'^sina_login_url/$', 'apps.third_party_login_app.views.get_qq_login_url',{'CALLBACK_URL':SINA_MOBILE_CALLBACK_URL}),
     url(r'^sina_login/$', 'apps.third_party_login_app.views.qq_login',{'CALLBACK_URL':SINA_MOBILE_CALLBACK_URL}),
     #手机facebook登陆
      url(r'^facebook_login_url/$', 'apps.third_party_login_app.views.get_qq_login_url',{'CALLBACK_URL':FACEBOOK_MOBILE_CALLBACK_URL}),
     url(r'^facebook_login/$', 'apps.third_party_login_app.views.qq_login',{'CALLBACK_URL':FACEBOOK_MOBILE_CALLBACK_URL}),
     #手机微信登录
      url(r'^weixin_login_url/$', 'apps.third_party_login_app.views.get_qq_login_url',{'CALLBACK_URL':WEIXIN_MOBILE_CALLBACK_URL}),
     url(r'^weixin_login/$', 'apps.third_party_login_app.views.qq_login',{'CALLBACK_URL':WEIXIN_MOBILE_CALLBACK_URL}),
    
    #消息页面                    
    url(r'^message/$', 'apps.message_app.views.message',{'template_name':'mobile_message.html'}),
    url(r'^message_list/$','apps.message_app.views.message_list',{'template_name': 'mobile_message.html'}),
    url(r'^follow_list/$','apps.message_app.views.get_follow_message',{'template_name': 'mobile_message.html'}),
    url(r'^comment_list/$', 'apps.friend_dynamic_app.views.comment_list',{'template_name':'mobile_message.html'}), 
     url(r'^agree_list/$', 'apps.friend_dynamic_app.views.agree_list',{'template_name': 'mobile_message.html'}),
     #更新权重                     
    url(r'^update_weight/$', 'apps.recommend_app.views.update_weight'),
    #手机充值
    url(r'^member/$', 'apps.pay_app.views.member',{'template_name':'mobile_recharge.html'}),  
    #获取免费获取拼爱币信息
    url(r'^get_free_pinloveicon/$', 'apps.user_score_app.views.get_free_pinloveicon',{'template_name':'mobile_mission.html'}),  
     url(r'^loggedin/', 'pinloveweb.views.loggedin',{'template_name':'mobile_recommend.html'}),
    #登出
    url(r'^logout/', 'pinloveweb.views.logout'),                
    url(r'^register/$','pinloveweb.views.register_user',{'template_name':'mobile_register.html'}),
    url(r'^auth/$','pinloveweb.views.auth_view',{'template_name':'mobile_login.html'}),
    url(r'^$','pinloveweb.views.login',{'template_name':'mobile_login.html','nextUrl':'loggedin'}),
    
    
)
