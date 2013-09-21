'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from apps.recommend_app.models import Grade, UserExpect, matchResult

admin.site.register(Grade)
admin.site.register(UserExpect)
admin.site.register(matchResult)
# admin.site.register(Message)
# admin.site.register(Friend,FriendAdmin)
# admin.site.register(new)
