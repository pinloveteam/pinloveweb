# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from apps.user_score_app.models import UserScore, UserScoreExchangeRelate,\
    UserScoreDtail
 
class UserScoreAdmin(admin.ModelAdmin):
    pass
class UserScoreExchangeRelateAdmin(admin.ModelAdmin):
    pass
class UserScoreDtailAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserScore,UserScoreAdmin)
admin.site.register(UserScoreExchangeRelate,UserScoreExchangeRelateAdmin)
admin.site.register(UserScoreDtail,UserScoreDtailAdmin)

