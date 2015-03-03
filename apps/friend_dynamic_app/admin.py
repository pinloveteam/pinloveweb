#-*- coding: utf-8 -*-
'''
Created on Jul 4, 2013
 
@author: jin
'''
from django.contrib import admin
from apps.friend_dynamic_app.models import FriendDynamicComment, FriendDynamic

class FriendDynamicAdmin(admin.ModelAdmin):
    list_display=('publishUser','type','publishTime')
    search_fields =('publishUser__username','type',)
    list_filter = ('type',)
class FriendDynamicCommentAdmin(admin.ModelAdmin):
    def get_frienddynamic_id(self, obj):
        return obj.friendDynamic.id
    get_frienddynamic_id.short_description = '动态id'
    def get_frienddynamic_username(self, obj):
        return obj.friendDynamic.publishUser.username
    list_display=('get_frienddynamic_id','reviewer','receiver','commentTime','isDelete','isRead')
    search_fields =('reviewer__username','receiver__username',)
    list_filter = ('isDelete','isRead')
              
admin.site.register(FriendDynamicComment,FriendDynamicCommentAdmin)
admin.site.register(FriendDynamic,FriendDynamicAdmin)
