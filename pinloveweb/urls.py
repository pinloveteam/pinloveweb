from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinlove.views.home', name='home'),
    # url(r'^pinlove/', include('pinlove.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Main Pages 
    url(r'^$', 'pinloveweb.views.login'),
    url(r'^account/login/', 'pinloveweb.views.login'), 
    url(r'^account/auth/', 'pinloveweb.views.auth_view'),
    url(r'^account/loggedin/', 'pinloveweb.views.loggedin'),
    url(r'^account/invalid/', 'pinloveweb.views.invalid_login'),
    url(r'^account/logout/', 'pinloveweb.views.logout'), 
    url(r'^account/register/', 'pinloveweb.views.register'), 
    url(r'^account/loggedout/', 'pinloveweb.views.loggedout')
)
