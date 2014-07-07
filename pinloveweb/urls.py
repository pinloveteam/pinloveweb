# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url, static
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

#user
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinlove.views.home', name='home'),
    # url(r'^pinlove/', include('pinlove.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     (r'^admin/doc/', include('django.contrib.admindocs.urls')),  
#     (r'^grappelli/',include('grappelli.urls')), 
#     (r'^grappelli/',include('grappelli.urls')), 
      url(r'^upload_avatar/', include('apps.upload_avatar.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/verification/$','apps.verification_app.views.income_valid'),
    url(r'^admin/', include(admin.site.urls)),
    
    # Main Pages 
    
    # Login and logout  
    url(r'^$', 'pinloveweb.views.login'),
    url(r'^account/login/', 'pinloveweb.views.login'), 
    url(r'^account/auth/', 'pinloveweb.views.auth_view'),
    url(r'^account/loggedin/', 'pinloveweb.views.loggedin'),
    url(r'^account/invalid/', 'pinloveweb.views.invalid_login'),
    url(r'^account/logout/', 'pinloveweb.views.logout'), 
    url(r'^account/loggedout/', 'pinloveweb.views.loggedout'),
    url(r'^account/forget_password/', 'pinloveweb.views.forget_password'),
    # Registration 
    url(r'^account/register/$', 'pinloveweb.views.register_user'), 
    url(r'^account/register_success/$', 'pinloveweb.views.register_success'),
    url(r'^account/verification/$', 'pinloveweb.views.register_verify'), 
    url(r'^account/check_register/$', 'pinloveweb.views.check_register'),
   url(r'^newCount/$', 'pinloveweb.views.newcount'),
    
    # User Profile 
    (r'^user/', include('apps.user_app.urls')), 
    # search models 
    (r'^search/', include('apps.search_app.urls')), 
    #recommend app
    (r'^recommend/', include('apps.recommend_app.urls')), 
     #game app
    (r'^game/', include('apps.game_app.urls')), 
     #publish_app
    (r'^publish/', include('apps.publish_app.urls')), 
     #verification_app
    (r'^verification/', include('apps.verification_app.urls')), 
    #notify_app
    (r'^message/', include('apps.message_app.urls')), 
    #dynamic_app
    (r'^dynamic/', include('apps.friend_dynamic_app.urls')), 
    #the_people_nearby
    (r'^the_people_nearby/', include('apps.the_people_nearby.urls')), 
    #user_score_app
    (r'^score/', include('apps.user_score_app.urls')), 
#      url(r'^celery_test/', 'apps.task_app.views.test_celery'),
####第三方登录###
    (r'^third_party_login/', include('apps.third_party_login_app.urls')),
    (r'^pay/', include('apps.pay_app.urls')),

     url(r'^test/$', 'pinloveweb.views.test'),
     #paypal
    (r'^pay/paypal/', include('paypal.standard.ipn.urls')),
    
    
    (r'^weixin', include('apps.weixin_app.urls')),
    (r'^alipay', include('apps.alipay_app.urls')),
)

#禁止搜索引擎收录
urlpatterns+=patterns('',
                       url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt")),
)
#网站信息
urlpatterns+=patterns('',
                       url(r'^web/$','pinloveweb.views.web',{'template_name': 'about.html'}),
#                        url(r'^web/privacy/$','pinloveweb.views.web',{'template_name': 'privacy.html'}),
#                        url(r'^web/about/$','pinloveweb.views.web',{'template_name': 'about.html'}),
#                        url(r'^web/contactus/$','pinloveweb.views.web',{'template_name': 'contactus.html'})
                      
)

if settings.DEBUG:
   urlpatterns += patterns('',
                          url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT },name="static"),
                           url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT },name="site_media"),
                          url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT },name="media"),
)
   
   
