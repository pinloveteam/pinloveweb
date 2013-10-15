'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from apps.recommend_app.models import Grade, UserExpect, MatchResult
class GradeAdmin(admin.ModelAdmin):
    list_display = ('user','heightweight', 'incomescore', 'incomeweight', 
                    'edcationscore', 'edcationweight', 'appearancescore',
                    'appearanceweight','characterweight','appearancesvote',)

    search_fields = ('user__username',)
#     filter_horizontal = ('user',)  ManyToManyField
#     list_filter = ('category',)
#     def get_username(self, obj):
#         return '%s'%(obj.user.username)
#     get_username.short_description = 'username'       

class UserExpectAdmin(admin.ModelAdmin):
     list_display = ('user','heighty1','heighty2','heighty3')
     search_fields = ('user__username',)
class MatchResultAdmin(admin.ModelAdmin):
     list_display = ('my','other','scoreMyself','scoreOther','macthScore')
     search_fields = ('my__username',)
#      ordering =('-macthScore')
admin.site.register(Grade,GradeAdmin)
admin.site.register(UserExpect,UserExpectAdmin)
admin.site.register(MatchResult,MatchResultAdmin)
# admin.site.register(Message)
# admin.site.register(Friend,FriendAdmin)
# admin.site.register(new)
