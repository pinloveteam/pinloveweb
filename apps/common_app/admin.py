#-*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''

from django.contrib import admin
from apps.common_app.models import School, Tag
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('ranking', 'name', 'type', )

    search_fields = ('name',)
#     filter_horizontal = ('user',)  ManyToManyField
    list_filter = ('type',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('content', )

    search_fields = ('content',)
    list_filter = ('group','value')
    
admin.site.register(School,SchoolAdmin)
admin.site.register(Tag,TagAdmin)


