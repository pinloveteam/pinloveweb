# -*- coding: utf-8 -*-
'''
Created on 2014年11月19日

@author: jin
'''
#个人基本详细
from django.forms.models import ModelForm
from apps.user_app.models import UserProfile
class InfoForm (ModelForm) : 
    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            from django.forms.fields import TypedChoiceField
            if isinstance(self.fields[key],TypedChoiceField):
                self.fields[key].choices=self.fields[key].choices[2:]
            self.fields[key].required = False
            self.fields[key].widget.attrs['class']='form-control'
            
    class Meta : 
        model = UserProfile  
        fields = ( 'height',  'income','education',)
        
        exclude = ('stateProvince','avatar_name','city', 'country', 'age','sunSign', 'zodiac','avatar_name_status',
                   'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress','gender', 'year_of_birth', 'month_of_birth', 'day_of_birth','ethnicGroup','bloodType',
         'maritalStatus', 'hasChild' ,'educationSchool','educationSchool', 'link', 'streetAddress','position','language',
                   ) 