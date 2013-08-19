'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from models import user_basic_profile,Dictionary
# class FriendAdmin(admin.ModelAdmin):
#     list_display=('myId','friendId','type')
#     search_fields =('myId','friendId','type')
#     fields =('myId','type','friendId')
admin.site.register(user_basic_profile)
admin.site.register(Dictionary)
# admin.site.register(Message)
# admin.site.register(Friend,FriendAdmin)
# admin.site.register(new)
