from django.conf.urls import patterns, url
urlpatterns=patterns('apps.game_app.views',
    url(r'^game_pintu/$', 'pintu'),
    url(r'^jigsaw/$', 'jigsaw',name="jigsaw"),
    
)