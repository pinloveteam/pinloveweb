from django.conf.urls import patterns, include, url, static
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#user
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinlove.views.home', name='home'),
    # url(r'^pinlove/', include('pinlove.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
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
    # Registration 
    url(r'^account/register/$', 'pinloveweb.views.register_user'), 
    url(r'^account/register_success/$', 'pinloveweb.views.register_success'),
    url(r'^account/verification/$', 'pinloveweb.views.register_verify'), 
    
    # User Profile 
    (r'^user/', include('apps.user_app.urls')), 
    # search models 
    (r'^search/', include('apps.user_app.urls')), 
    
)



if settings.DEBUG:
   urlpatterns += patterns('',
                          url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT },name="static"),
                           url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT },name="site_media"),
                          url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT },name="update"),
)
