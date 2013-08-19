# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.user_app.models import user_basic_profile, user_contact_link,\
    user_appearance, user_study_work, user_hobby_interest,\
    user_family_information, user_personal_habit, user_family_life
from apps.user_app import user_validators

#个人基本详细
class UserBasicProfileForm (ModelForm) : 
    def __init__(self, *args, **kwargs):
        super(UserBasicProfileForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False
    class Meta : 
        model = user_basic_profile  
        fields = ( 'gender', 'photo','year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'education', 'link', 'streetAddress','position','language',)
        
        exclude = ('stateProvince','city', 'country', 'age','sunSign', 
            'zodiac') 

#个人联系方式  
class UserContactForm(ModelForm):
    mobileNumber=forms.RegexField(label=_("手机号:"),regex=r'^1[3|4|5|8][0-9]\d{4,8}$'
                                   ,help_text='',error_messages={
            'invalid':  _(u"手机号码填写不正确！")})
    IDCardNumber=forms.RegexField(label=_("身份证号:"),regex=r'^\d{18}$'
                                   ,help_text='',error_messages={
            'invalid':  _(u"身份证位数或格式不正确！")})
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
        model=user_contact_link
        fields=('trueName','mobileNumber','IDCardNumber','QQ','MSN','stateProvinceHome','CountryHome','cityHome')
        exclude=('stateProvinceHome','CountryHome','cityHome')
        
    def clean_IDCardNumber(self):   
         IDCardNumber = self.cleaned_data["IDCardNumber"]  
         if len(IDCardNumber) <1:
             return IDCardNumber 
         result=user_validators.checkIdcard(IDCardNumber)
         if result!='验证通过!':
              raise forms.ValidationError(result)     
         else:
             return IDCardNumber

#个人外貌       
class UserAppearanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAppearanceForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
    class Meta:
        model=user_appearance
        field=('self_evaluation','weight','hairStyle','hairColor',
               'face','eyeColor','bodyShape',)
        exclude=('user')
#工作学习   
class UserStudyWorkForm(ModelForm): 
    def __init__(self, *args, **kwargs):
        super(UserStudyWorkForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
    class Meta:
        model=user_study_work
        field=('jobIndustry','jobTitle','COMPANY_TYPE_CHOICE','workStatus',
               'companyName','educationCountry','educationSchool','isStudyAbroad',)
        exclude=('user')
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
        model=user_hobby_interest
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
        model=user_personal_habit
        field=('belief','isSmoke','isDrink','beddingTime',
               'pet','character',)
        exclude=('user')
 # 家庭情况      
class UserFamilyInformationForm(ModelForm):
     def __init__(self, *args, **kwargs):
        super(UserFamilyInformationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
     class Meta:
        model=user_family_information
        field=('monthlyExpense','isOnlyChild','hasCar','hasHouse',
               'financialCondition','parentEducation',)
        exclude=('user')
#对未来期望        
class UserFamilyLifeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserFamilyLifeForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
    class Meta:
        model=user_family_life
        field=('liveWithParent','liveWithParent',)
        exclude=('user')
        


