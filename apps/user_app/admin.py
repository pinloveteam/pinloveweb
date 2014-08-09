# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from models import UserProfile
from django.db import  transaction
from apps.user_app.models import Follow
from django.conf import settings
from apps.recommend_app.models import Grade
from django import forms
'''
  基本信息
'''
class UserBasicProfile(UserProfile):
    class Meta:
        proxy = True
        app_label = 'user_basic_profile'
        verbose_name = u'用户基本信息' 
        verbose_name_plural = u'用户基本信息'
        
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
        app_label = 'user_appearance'
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
            return u'<img src="%s" />' %(settings.MEDIA_URL+self.avatar_name+'-250.jpeg')
    image_img.short_description = '头像'
    image_img.allow_tags = True 
    
    class Meta:
        proxy = True
        app_label = 'avatar_check'
        verbose_name = u'头像审核' 
        verbose_name_plural = u'头像审核'
#     appearancescore=models.FloatField(verbose_name=u"外貌分数",null=True)
        
# class AppearancScore(Grade): 
#      author = models.ForeignKey(AvatarCheck)   
#      class Meta:
#         proxy = True
#         verbose_name = u'相貌打分' 
#         verbose_name_plural = u'相貌打分'
           
class AvatarCheckForm(forms.ModelForm):
    from django.core.validators import MaxValueValidator,MinValueValidator
    appearancescore=forms.FloatField(label=u"外貌分数",validators = [MinValueValidator(0), MaxValueValidator(100)],help_text=u'分数在[0,100]区间')
    class Meta:
        model=AvatarCheck
#     def __init__(self, *args, **kwargs):
#         super(AvatarCheckForm, self).__init__(*args, **kwargs)
#         # Here we will redefine our test field.
#         self.fields['appearancescore'] = forms.FloatField(label=u"外貌分数",)
# class AppearancScoreForm(forms.ModelForm):
# #     appearancescore=models.FloatField(verbose_name=u"外貌分数",null=True)
#     class Meta:
#         model=AppearancScore
#         
#     def __init__(self, *args, **kwargs):
#         super(AvatarCheckForm, self).__init__(*args, **kwargs)
#  
  
class AvatarCheckAdmin(admin.ModelAdmin):
    form = AvatarCheckForm
    list_display=('user','avatar_name_status','get_appearancescore')
    search_fields =('user__username',)
    readonly_fields=('image_img','avatar_name',)
    list_filter=('avatar_name_status',)    
    fields =('user','image_img','avatar_name','avatar_name_status','appearancescore')
    def __init__(self, *args, **kwargs):
        super(AvatarCheckAdmin, self).__init__(*args, **kwargs)
#         # Here we will redefine our test field.
#         self.fields['appearancescore'] = models.FloatField(verbose_name=u"外貌分数",)
#     def change_view(self, request, object_id, form_url='', extra_context=None):
#         self.appearancescore=Grade.objects.get(user=self.user).appearancescore
#         return super(AvatarCheckAdmin, self).change_view(request, object_id,
#             form_url, extra_context=extra_context)
       
    def get_appearancescore(self,instance):
        return Grade.objects.get(user=instance.user).sysappearancescore
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
    """
     重写save
    """
    @transaction.commit_on_success  
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()
        user_1=obj.user
        appearancescore=form.cleaned_data['appearancescore']
        if  Grade.objects.filter(user=user_1,appearancescore__lte=0).exists():
            Grade.objects.filter(user=user_1).update(appearancescore=appearancescore,sysappearancescore=appearancescore)
        else:
             grade=Grade.objects.get(user=user_1)
             from apps.recommend_app.recommend_util import cal_user_vote
             data=cal_user_vote(None,None,appearancescore,grade.appearancescore,grade.appearancesvote,0,sysappearancescore=grade.sysappearancescore)
             Grade.objects.filter(user=user_1).update(appearancescore=data['score'],sysappearancescore=appearancescore)
            
        
        #头像认证通过得分
        from apps.user_score_app.method import get_score_by_avatar_check
        get_score_by_avatar_check(user_1.id)
class FollowAdmin(admin.ModelAdmin):
    list_display=('my','follow',)
    search_fields =('my__username','follow__username',)
    fields =('my','follow',)
#     list_filter=('type','hasCar','hasHouse','financialCondition','parentEducation',)   

admin.site.register(UserBasicProfile,UserBasicProfileAdmin)
admin.site.register(UserAppearance,UserAppearanceAdmin)
admin.site.register(UserStudyWork,UserStudyWorkAdmin)
admin.site.register(UserFamilyInformation,UserFamilyInformationAdmin)
admin.site.register(UserPersonalHabit,UerPersonalHabitAdmin)
admin.site.register(AvatarCheck,AvatarCheckAdmin)
admin.site.register(Follow,FollowAdmin)
# admin.site.register(Dictionary)
# admin.site.register(Message)
# admin.site.register(new)
