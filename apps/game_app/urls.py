from django.conf.urls import patterns, url
urlpatterns=patterns('apps.game_app.views',
    url(r'^game_pintu/$','pintu'),
    url(r'^jigsaw/$','jigsaw',name="jigsaw"),
    url(r'^jigsaw_mobi/$','jigsaw_mobi'),
    url(r'^confirm_request_life/$','confirm_request_life'),
   # url(r'^pintu_for_facebook/$','pintu_for_facebook'),
   url(r'^reset_game/$','reset_game_cache'),
    url(r'^recommend_history/$','recommend_history'),
)
urlpatterns += patterns('apps.third_party_login_app.views',
url(r'^pintu_for_facebook/$','pintu_for_facebook'),
url(r'^debug_pintu_cache/$','debug_pintu_cache'),
url(r'^debug_update/$','debug_update'),
url(r'^test_get_code/$','test_get_code'),
url(r'^feed_on_wall/$','feed'),

)