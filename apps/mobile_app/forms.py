#-*- coding: UTF-8 -*- 
'''
Created on 2014年12月23日

@author: jin
'''
from apps.user_app.models import UserProfile
from django.forms.models import ModelForm
from django import forms
'''
个人信息编辑页面
'''
class UserProfileMbolieForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileMbolieForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        for key in self.fields:
            from django.forms.fields import TypedChoiceField
            if isinstance(self.fields[key],TypedChoiceField):
                self.fields[key].choices=self.fields[key].choices[1:]
            self.fields[key].required = False
            self.fields[key].widget.attrs['class']='form-control'
        
    #判断出生年月日是否正确
    def clean_day_of_birth(self):
        day_of_birth=self.cleaned_data['day_of_birth']
        month_of_birth=self.cleaned_data['month_of_birth']
        year_of_birth=self.cleaned_data['year_of_birth']
        if not((day_of_birth==-1 and month_of_birth==-1 and year_of_birth==-1) or (day_of_birth!=-1 and month_of_birth!=-1 and year_of_birth!=-1)):
#             self._errors['year_of_birth'] =self.error_class(u'请正确填写出生日期!')
            raise  forms.ValidationError(u'请正确填写出生日期!')
        return day_of_birth
    

    def clean_country(self):
        if self.cleaned_data['country'] in [u'请选择']:
            self.cleaned_data['country']=None
            return None
        else:
            return self.cleaned_data['country']
        
    def clean_stateProvince(self):
        if self.cleaned_data['stateProvince'] in [u'请选择']:
            self.cleaned_data['stateProvince']=None
            return None
        else:
            return self.cleaned_data['stateProvince']
        
            
    def clean_city(self):
        if self.cleaned_data['city'] in [u'请选择']:
            self.cleaned_data['city']=None
        city=self.cleaned_data['city']
        stateProvince=self.cleaned_data['stateProvince']
        country=self.cleaned_data['country']
        if not ((city==None and stateProvince==None and country==None)or(city!=None and stateProvince!=None and country!=None)):
            raise  forms.ValidationError(u'请正确填居住地!')
        return city
        
            
    class Meta : 
        model = UserProfile  
        fields = ( 'income','weight','jobIndustry',
        'height', 'education','year_of_birth', 'month_of_birth', 'day_of_birth','educationSchool','educationSchool_2', 
         'country','stateProvince','city',)
        
        exclude = ('avatar_name', 'sunSign', 'zodiac','avatar_name_status',
                   'self_evaluation','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress', 'maritalStatus', 'hasChild' ,
                   'link', 'streetAddress','position','language','ethnicGroup','bloodType','age', 'gender',
                   ) 
