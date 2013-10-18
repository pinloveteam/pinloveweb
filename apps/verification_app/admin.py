# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2013

@author: jin
'''
from apps.user_app.models import UserVerification, UserProfile, UserContactLink
from django.conf import settings
from django.contrib import admin
'''
  身份审核
'''
class IDCardCheck(UserVerification):
    def image_img(self):
#             print  u'<img src="%s" />' %(settings.MEDIA_URL+self.IDCardPicture.name)
            return u'<img src="%s" />' %(settings.MEDIA_URL+self.IDCardPicture.name)
    image_img.short_description = '身份（护照）图'
    image_img.allow_tags = True 
    
    class Meta:
        proxy = True
        verbose_name = u'身份证(护照)审核' 
        verbose_name_plural = u'身份证(护照)审核'
        
class IDCardCheckAdmin(admin.ModelAdmin):
    list_display=('user','IDCardValid',)
    search_fields =('user__username',)
    readonly_fields=('image_img','user','get_truename','get_IDCardChoice','get_IDCardNumber',)
    list_filter=('IDCardValid',)    
    fields =('user','get_truename','get_IDCardChoice','get_IDCardNumber','image_img','IDCardValid',)
    def get_IDCardChoice(self,obj):
        return UserContactLink.objects.get(user=obj.user).get_IDCardChoice_display()
    get_IDCardChoice.short_description = '证件类型'
    def get_truename(self,obj):
        return UserContactLink.objects.get(user=obj.user).etrueName
    get_truename.short_description = '真实姓名'
    def get_IDCardNumber(self,obj):
        return UserContactLink.objects.get(user=obj.user).IDCardNumber
    get_IDCardNumber.short_description = '证件号'
       
    #默认过滤
    def changelist_view(self, request, extra_context=None):
        if not request.GET.has_key('IDCardValid__exact'):
            q = request.GET.copy()
            q['IDCardValid__exact'] = '2'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(IDCardCheckAdmin,self).changelist_view(request, extra_context=extra_context)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "IDCardValid":
            kwargs['choices'] = (
               ('3',"审核通过"),('4',"审核未通过"),
            )
        return super(IDCardCheckAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    
    
'''
学历审核
'''
class EducationCheck(UserVerification):
    def image_img(self):
#             print  u'<img src="%s" />' %(settings.MEDIA_URL+self.IDCardPicture.name)
            return u'<img src="%s" />' %(settings.MEDIA_URL+self.educationPicture.name)
    image_img.short_description = '学历证明'
    image_img.allow_tags = True 
    class Meta:
        proxy = True
        verbose_name = u'学历审核' 
        verbose_name_plural = u'学历审核'
        
class EducationCheckAdmin(admin.ModelAdmin):
    list_display=('user','educationValid',)
    search_fields =('user__username',)
    readonly_fields=('image_img','user','get_education','get_educationSchool')
    list_filter=('educationValid',)    
    fields =('user','get_education','get_educationSchool','image_img','educationValid')
       
    def get_education(self,obj):
        return UserProfile.objects.get(user=obj.user).get_education_display()
    get_education.short_description = '学历'
    def get_educationSchool(self,obj):
        return UserProfile.objects.get(user=obj.user).educationSchool
    get_educationSchool.short_description = '毕业学校'


    #默认过滤
    def changelist_view(self, request, extra_context=None):
        if not request.GET.has_key('educationValid__exact'):
            q = request.GET.copy()
            q['educationValid__exact'] = '2'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(EducationCheckAdmin,self).changelist_view(request, extra_context=extra_context)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "IDCardValid":
            kwargs['choices'] = (
               ('3',"审核通过"),('4',"审核未通过"),
            )
        return super(EducationCheckAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    def __init__(self, *args, **kwargs):
        super(EducationCheckAdmin, self).__init__(*args, **kwargs)
        
'''
收入审核
'''
class IncomeCheck(UserVerification):
    def image_img(self):
#             print  u'<img src="%s" />' %(settings.MEDIA_URL+self.IDCardPicture.name)
            return u'<img src="%s" />' %(settings.MEDIA_URL+self.incomePicture.name)
    image_img.short_description = '收入证明'
    image_img.allow_tags = True 
    class Meta:
        proxy = True
        verbose_name = u'收入审核' 
        verbose_name_plural = u'收入审核'
        
class IncomeCheckAdmin(admin.ModelAdmin):
    list_display=('user','incomeValid',)
    search_fields =('user__username',)
    readonly_fields=('image_img','user','get_income',)
    list_filter=('incomeValid',)    
    fields =('user','get_income','image_img','incomeValid',)
       
    def get_income(self,obj):
        return UserProfile.objects.get(user=obj.user).income
    get_income.short_description = '收入'


    #默认过滤
    def changelist_view(self, request, extra_context=None):
        if not request.GET.has_key('incomeValid__exact'):
            q = request.GET.copy()
            q['incomeValid__exact'] = '2'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(IncomeCheckAdmin,self).changelist_view(request, extra_context=extra_context)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "incomeValid":
            kwargs['choices'] = (
               ('3',"审核通过"),('4',"审核未通过"),
            )
        return super(IncomeCheckAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    
admin.site.register(IDCardCheck,IDCardCheckAdmin)
admin.site.register(EducationCheck,EducationCheckAdmin)
admin.site.register(IncomeCheck,IncomeCheckAdmin)