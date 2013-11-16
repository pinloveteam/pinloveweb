from django.conf.urls import patterns, url
urlpatterns=patterns('apps.the_people_nearby.views',
    url(r'^the_people_nearby/$', 'the_people_nearby'),
)