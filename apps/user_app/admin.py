# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from models import UserProfile,Dictionary
from django.db import models
from apps.user_app.models import Friend
from django.conf import settings
from apps.recommend_app.models import Grade
'''
  基本信息
'''
class UserBasicProfileAdmin(admin.ModelAdmin):
    list_display=('user','gender','get_birthday','age','height','education','educationSchool','income',)
    search_fields =('user__username','educationSchool',)
    readonly_fields=('age','link',)
    fields =('user','gender','year_of_birth','month_of_birth','day_of_birth',
             'age','sunSign','zodiac','ethnicGroup','bloodType','height','maritalStatus',
             'hasChild','link','country','stateProvince','city','streetAddress',
             'education','educationSchool','income','position','language','avatar_name',)
    list_filter=('gender','education','income','age')
    def get_birthday(self, obj):
        return '%s-%s-%s'%(obj.year_of_birth,obj.month_of_birth,obj.day_of_birth)
    get_birthday.short_description = '出生时间'
'''
  外貌
'''
class UserAppearance(UserProfile):
    class Meta:
        proxy = True
        verbose_name = u'外貌' 
        verbose_name_plural = u'外貌'
class UserAppearanceAdmin(admin.ModelAdmin):    
    list_display=('user','weight','hairStyle','hairColor','face','eyeColor','bodyShape','self_evaluation',)
    search_fields =('user__username',)
    fields =('user','weight','hairStyle','hairColor','face','eyeColor','bodyShape','self_evaluation',)
'''
  学习生活
'''
class UserStudyWork(UserProfile):
    class Meta:
        proxy = True
        verbose_name = u'学习生活' 
        verbose_name_plural = u'学习生活'
class UserStudyWorkAdmin(admin.ModelAdmin):
    list_display=('user','jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry',)
    search_fields =('user__username','companyName',)
    fields =('user','jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry',)
    list_filter=('companyType','workStatus','jobTitle',)
    
'''
  个人习惯
'''
class UserPersonalHabit(UserProfile):
    class Meta:
        proxy = True
        verbose_name = u'个人习惯' 
        verbose_name_plural = u'个人习惯'
class UerPersonalHabitAdmin(admin.ModelAdmin):
    list_display=('user','belief','isSmoke','beddingTime','pet','character',)
    search_fields =('user__username','pet','character',)
    fields =('user','jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry',)
    list_filter=('isSmoke','isDrink','workStatus','beddingTime','belief',)   

'''
  家庭信息
'''
class UserFamilyInformation(UserProfile):
    class Meta:
        proxy = True
        verbose_name = u'家庭信息' 
        verbose_name_plural = u'家庭信息'
class UserFamilyInformationAdmin(admin.ModelAdmin):
    list_display=('user','monthlyExpense','isOnlyChild','hasCar','hasHouse','character','financialCondition','parentEducation',)
    search_fields =('user__username',)
    fields =('user','monthlyExpense','isOnlyChild','hasCar','hasHouse','character','financialCondition','parentEducation','liveWithParent','likeChild')
    list_filter=('isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',)   


'''
  头像审核
'''
class AvatarCheck(UserProfile):
#     def __init__(self, *args, **kwargs):
#           STATUS_CHOICES = (('3',"审核通过"),('4',"审核未通过"),)
#           self.STATUS_CHOICES =STATUS_CHOICES
# #     avatar_name_status=models.CharField(verbose_name=r"头像状态",max_length=2, choices=STATUS_CHOICES,default='3')
    def image_img(self):
            return u'<img src="%s" />' %(settings.MEDIA_URL+'user_img/image.png')
    image_img.short_description = '头像'
    image_img.allow_tags = True
    class Meta:
        proxy = True
        verbose_name = u'头像审核' 
        verbose_name_plural = u'头像审核'
class AvatarCheckAdmin(admin.ModelAdmin):
    list_display=('user','avatar_name_status','get_score')
    search_fields =('user__username',)
    readonly_fields=('image_img','avatar_name',)
    list_filter=('avatar_name_status',)    
    fields =('user','image_img','avatar_name','avatar_name_status',)
    #默认过滤
    def changelist_view(self, request, extra_context=None):
        if not request.GET.has_key('avatar_name_status__exact'):
            q = request.GET.copy()
            q['avatar_name_status__exact'] = '2'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(AvatarCheckAdmin,self).changelist_view(request, extra_context=extra_context)
#     def get_score(self, obj):
#         grade=Grade.objects.filter(user=obj.user)
#         return '%s'%(grade.heightweight)
#     get_score.short_description = '分数'     
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "avatar_name_status":
            kwargs['choices'] = (
               ('3',"审核通过"),('4',"审核未通过"),
            )
        return super(AvatarCheckAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
class FriendAdmin(admin.ModelAdmin):
    list_display=('my','friend',)
    search_fields =('my__username','friend__username',)
    fields =('my','friend','type')
#     list_filter=('type','hasCar','hasHouse','financialCondition','parentEducation',)   

admin.site.register(UserProfile,UserBasicProfileAdmin)
admin.site.register(UserAppearance,UserAppearanceAdmin)
admin.site.register(UserStudyWork,UserStudyWorkAdmin)
admin.site.register(UserFamilyInformation,UserFamilyInformationAdmin)
admin.site.register(UserPersonalHabit,UerPersonalHabitAdmin)
admin.site.register(AvatarCheck,AvatarCheckAdmin)
admin.site.register(Friend,FriendAdmin)
# admin.site.register(Dictionary)
# admin.site.register(Message)
# admin.site.register(new)
