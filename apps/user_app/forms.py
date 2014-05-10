# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.user_app.models import UserProfile, UserContactLink, UserHobbyInterest
from apps.user_app import user_validators
'''
个人信息编辑页面
'''
class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['age'].widget.attrs['readonly'] = True
            self.fields['gender'].choices=((self.fields['gender'].initial,dict(self.fields['gender'].choices)[self.fields['gender'].initial]),)
            self.fields['gender'].widget.attrs['readonly'] = True
        for key in self.fields:
            self.fields[key].required = False
            self.fields[key].widget.attrs['class']='form-input'
    
    def clean_age(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.age
        else:
            return self.cleaned_data['age']
        
    def clean_gender(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.gender
        else:
            return self.cleaned_data['gender']
        
    #判断出生年月日是否正确
    def clean_day_of_birth(self):
        day_of_birth=self.cleaned_data['day_of_birth']
        month_of_birth=self.cleaned_data['month_of_birth']
        year_of_birth=self.cleaned_data['year_of_birth']
        if not((day_of_birth==-1 and month_of_birth==-1 and year_of_birth==-1) or (day_of_birth!=-1 and month_of_birth!=-1 and year_of_birth!=-1)):
            raise  forms.ValidationError(u'请正确填写出生日期!')
        else:
            return day_of_birth
    
    class Meta : 
        model = UserProfile  
        fields = ( 'gender', 'income','weight','jobIndustry','age',
        'height', 'education','year_of_birth', 'month_of_birth', 'day_of_birth','educationSchool','educationSchool_2' )
        
        exclude = ('stateProvince','avatar_name','city', 'country', 'sunSign', 'zodiac','avatar_name_status',
                   'self_evaluation','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress', 'maritalStatus', 'hasChild' ,
                   'link', 'streetAddress','position','language','ethnicGroup','bloodType',
                   ) 
#         widgets = { 
#             'gender': forms.TextInput(),
#         }   


#个人基本详细
class UserBasicProfileForm (ModelForm) : 
    def __init__(self, *args, **kwargs):
        super(UserBasicProfileForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False
    class Meta : 
        model = UserProfile  
        fields = ( 'gender', 'year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'education','educationSchool', 'link', 'streetAddress','position','language',)
        
        exclude = ('stateProvince','avatar_name','city', 'country', 'age','sunSign', 'zodiac','avatar_name_status',
                   'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress',
                   ) 

#个人联系方式  
class UserContactForm(ModelForm):
    IDRegex=r'^\d{18}$'
    mobileNumber=forms.RegexField(label=_("手机号:"),regex='^[0-9]\d{6,11}$'
                                   ,help_text='',error_messages={
            'invalid':  _(u"手机号码填写不正确！")})
    IDCardNumber=forms.RegexField(label=_("身份证号:"),regex=r'^(\d{18})|(..\d{5,7})$'
                                   ,help_text='',error_messages={
            'invalid':  _(u"证件位数或格式不正确！")})
    QQ=forms.RegexField(label=_("QQ:"),regex=r'^[1-9][0-9]{4,}$'
                                   ,help_text='',error_messages={
            'invalid':  _(u"QQ格式不正确！")})
    MSN=forms.RegexField(label=_("MSN:"),regex=r'^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$'
                                   ,help_text='',error_messages={
            'invalid':  _(u"MSN格式不正确！")})
    
    def __init__(self, *args, **kwargs):
        super(UserContactForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
            
                
    class Meta:
        model=UserContactLink
        fields=('IDCardChoice','trueName','mobileNumber','IDCardNumber','QQ','MSN','stateProvinceHome','CountryHome','cityHome')
        exclude=('stateProvinceHome','CountryHome','cityHome')
        
    def clean_IDCardNumber(self): 
         IDCardChoice = self.cleaned_data["IDCardChoice"] 
         IDCardNumber = self.cleaned_data["IDCardNumber"]  
         if len(IDCardNumber.rstrip()) <1:
             return IDCardNumber 
         if IDCardChoice==0:
             result=user_validators.checkIdcard(IDCardNumber)
             if result!='验证通过!':
                 raise forms.ValidationError(result)     
             else:
                 return IDCardNumber
         if IDCardChoice==1:
             result=user_validators.checkPassport(IDCardNumber)
             if result!=True:
                 raise forms.ValidationError(result)    
             else :
                 return IDCardNumber


#个人外貌       
class UserAppearanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAppearanceForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
    class Meta:
        model=UserProfile
        field=('self_evaluation','weight','hairStyle','hairColor',
               'face','eyeColor','bodyShape',)
        exclude=('user','avatar_name_status',
                 'gender', 'avatar_name','year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'education','educationSchool', 'link', 'streetAddress','position','language',
        'stateProvince','city', 'country', 'age','sunSign', 'zodiac',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress',
        )
#工作学习   
class UserStudyWorkForm(ModelForm): 
    def __init__(self, *args, **kwargs):
        super(UserStudyWorkForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
    class Meta:
        model=UserProfile
        field=('jobIndustry','jobTitle','companyType','workStatus',
               'companyName','educationCountry','isStudyAbroad',)
        exclude=('user','avatar_name_status',
                 'gender', 'avatar_name','year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'education','educationSchool', 'link', 'streetAddress','position','language',
        'stateProvince','city', 'country', 'age','sunSign', 'zodiac',
        'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress',)
        widgets = {
                   'isStudyAbroad': forms.RadioSelect(attrs={'cols':20,'rows':20},choices=((True, u'是'), (False, u'否') ), )
                   }
        
#兴趣
class UserHobbyInterestForm(ModelForm): 
    def __init__(self, *args, **kwargs):
        super(UserHobbyInterestForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
    class Meta:
        model=UserHobbyInterest
        field=('sport','food','book','movice',
               'TVShow','recreation','travel',)
        exclude=('user')
#个人习惯      
class UserPersonalHabitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserPersonalHabitForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
    class Meta:
        model=UserProfile
        field=('belief','isSmoke','isDrink','beddingTime',
               'pet','character',)
        exclude=('user','avatar_name_status',
                 'gender', 'avatar_name','year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'education','educationSchool', 'link', 'streetAddress','position','language',
        'stateProvince','city', 'country', 'age','sunSign', 'zodiac',
        'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress',)
 # 家庭情况      
class UserFamilyInformationForm(ModelForm):
     def __init__(self, *args, **kwargs):
        super(UserFamilyInformationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
     class Meta:
        model=UserProfile
        field=('monthlyExpense','isOnlyChild','hasCar','hasHouse',
               'financialCondition','parentEducation',)
        exclude=('user','avatar_name_status',
                 'gender', 'avatar_name','year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'education','educationSchool', 'link', 'streetAddress','position','language',
        'stateProvince','city', 'country', 'age','sunSign', 'zodiac',
        'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'liveWithParent','likeChild','lastLoginAddress',)
#对未来期望        
# class UserFamilyLifeForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(UserFamilyLifeForm, self).__init__(*args, **kwargs)
#         for key in self.fields:
#             self.fields[key].required = False
#     class Meta:
#         model=UserProfile
#         field=('liveWithParent','liveWithParent',)
#         exclude=('user')
#         


class PhotoCheck(ModelForm):
      def __init__(self, *args, **kwargs):
        super(UserFamilyInformationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
      class Meta:
        model=UserProfile
        field=('avatar_name_status', )
        exclude=('user','avatar_name',
                 'gender','year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'education','educationSchool', 'link', 'streetAddress','position','language',
        'stateProvince','city', 'country', 'age','sunSign', 'zodiac',
        'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'liveWithParent','likeChild','lastLoginAddress',)