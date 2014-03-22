#-*- coding: UTF-8 -*- 
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.game_app.views',
    url(r'^game_pintu/$','pintu'),
    url(r'^jigsaw/$','jigsaw',name="jigsaw"),
    url(r'^jigsaw_mobi/$','jigsaw_mobi'),
    url(r'^confirm_request_life/$','confirm_request_life'),
)
#debug  facebook 拼图
urlpatterns +=patterns('apps.game_app.views',
                       
   url(r'^reset_game/$','reset_game_cache'),
#     url(r'^recommend_history/$','recommend_history'),
    #备份拼图的cache
    url(r'^backup_pintu_cache/$','backup_pintu_cache'),
    #还原拼图的cache
     url(r'^restore_backup_pintu_cache/$','restore_backup_pintu_cache'),
     #加游戏次数
     url(r'^add_user_count/$','add_user_count'),
     url(r'^invite_in_day/$','invite_in_day'),
     #########test##############
     url(r'^tset_match/$','tset_match'),
     
)
urlpatterns += patterns('apps.third_party_login_app.views',
url(r'^pintu_for_facebook/$','pintu_for_facebook'),
url(r'^pintu_for_facebook_android/$','pintu_for_facebook_android'),

url(r'^debug_pintu_cache/$','debug_pintu_cache'),
url(r'^debug_update/$','debug_update'),
url(r'^test_get_code/$','test_get_code'),
url(r'^feed_on_wall/$','feed'),

)