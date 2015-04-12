# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from apps.task_app.models import EmailRecommendHistory, TaskRecode
from django.http.response import HttpResponse
from django.conf.urls import patterns

class EmailRecommendHistoryAdmin(admin.ModelAdmin):
    list_display=('user','recommender','time')
    search_fields =('user__username',)
    
class TaskRecodeAdmin(admin.ModelAdmin):
    list_display=('result','content','time')
    search_fields =('content',)
    list_filter=('result',)    
    
admin.site.register(EmailRecommendHistory,EmailRecommendHistoryAdmin)
admin.site.register(TaskRecode,TaskRecodeAdmin)


# def my_view(request):
#     return HttpResponse("Hello!")
# 
# def get_admin_urls(urls):
#     def get_urls():
#         my_urls = patterns('',
#             (r'^my_view/$', admin.site.admin_view(my_view))
#         )
#         return my_urls + urls
#     return get_urls
# 
# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls


