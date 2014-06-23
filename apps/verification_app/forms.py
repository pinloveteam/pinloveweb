# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.user_app.models import UserProfile, UserContactLink
from apps.user_app import user_validators

'''
身份证验证
'''
class IDCardValidForm(ModelForm):
    IDRegex=r'^\d{18}$'
    IDCardNumber=forms.RegexField(label=_("身份证号:"),regex=r'^(\d{18})|(..\d{5,7})$'
                                   ,help_text='',error_messages={
            'invalid':  _(u"证件位数或格式不正确！")})
    IDCardPicture=forms.ImageField()
    def __init__(self, *args, **kwargs):
        super(IDCardValidForm, self).__init__(*args, **kwargs)
        self.fields['trueName'].required = False
        self.fields['IDCardChoice'].choices=((u'', u'请选择'),(0,'身份证'),(1,'护照'),)
        self.fields['IDCardChoice'].widget.attrs["class"]="form-label"
        self.fields['IDCardPicture'].widget.attrs["style"] = "display:inline-block;"
        
        self.fields['IDCardChoice'].required=True      
    class Meta:
        model=UserContactLink
        fields=('IDCardChoice','trueName','IDCardNumber',)
        exclude=('stateProvinceHome','CountryHome','cityHome','QQ','MSN','mobileNumber')
       
   
        
    def clean_IDCardNumber(self): 
         try:
             IDCardChoice = self.cleaned_data["IDCardChoice"] 
         except Exception as e:
             return
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

'''
学历证验证
'''
class EducationValidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EducationValidForm,self).__init__(*args, **kwargs)
        self.fields['education'].choices=((u'',u'请选择'),(0,r'大专以下'),(1,r'大专'),(2,r'本科'),(3,r'硕士 '),(4,r'博士 '),)
        self.fields['education'].required=True
        self.fields['educationPicture'].widget.attrs["style"] = "display:inline-block;"
        self.fields['educationPicture2'].widget.attrs["style"] = "display:inline-block;"
    educationPicture=forms.ImageField()
    educationPicture2=forms.ImageField()
    class Meta:
        model=UserProfile
        fields = ('education','educationSchool','educationSchool_2',)
        exclude = ('gender', 'year_of_birth', 'month_of_birth', 'day_of_birth', 'income','ethnicGroup','bloodType',
        'height', 'maritalStatus', 'hasChild' ,'stateProvince','avatar_name','city', 'country', 'age','sunSign', 'zodiac','avatar_name_status',
                   'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild', 'link', 'streetAddress','position','language',
                   ) 
'''
收入证验证
'''
class IncomeValidForm(ModelForm):
    incomePicture=forms.ImageField(label="收入证明")
    def __init__(self, *args, **kwargs):
        super(IncomeValidForm, self).__init__(*args, **kwargs)
        self.fields['income'].required = True
        self.fields['incomePicture'].widget.attrs["style"] = "display:inline-block;"
    class Meta:
        model=UserProfile
        fields = ('income',)
        exclude = ('gender', 'year_of_birth', 'month_of_birth', 'day_of_birth', 'ethnicGroup','bloodType','education','educationSchool',
        'height', 'maritalStatus', 'hasChild' ,'stateProvince','avatar_name','city', 'country', 'age','sunSign', 'zodiac','avatar_name_status',
                   'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild', 'link', 'streetAddress','position','language',
                   ) 