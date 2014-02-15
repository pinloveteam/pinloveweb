from django.conf.urls import patterns, url
urlpatterns=patterns('apps.game_app.views',
    url(r'^game_pintu/$','pintu'),
    url(r'^jigsaw/$','jigsaw',name="jigsaw"),
    url(r'^confirm_request_life/(.+)/$','confirm_request_life'),
   # url(r'^pintu_for_facebook/$','pintu_for_facebook'),
    
)
urlpatterns += patterns('apps.third_party_login_app.views',
url(r'^pintu_for_facebook/$','pintu_for_facebook')
)