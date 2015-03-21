# -*- coding: utf-8 -*-
'''
Created on 2014年11月23日

@author: jin
'''
from django.contrib import admin
from apps.weixin_app.models import ScoreRank
        
class WeiXinScoreRankAdmin(admin.ModelAdmin):
    list_display=('my','other','nickname','score','time',)
    fields =('my','other','nickname','score','time',)
    list_filter=('my',)
    search_fields =('nickname',)
      

admin.site.register(ScoreRank,WeiXinScoreRankAdmin)
