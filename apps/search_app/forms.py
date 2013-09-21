# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.user_app.models import UserProfile, user_contact_link,user_hobby_interest
from apps.user_app import user_validators
class AdvanceSearchForm(ModelForm):
    
    class Meta:
        model=UserProfile
        fields = ('education','income','sunSign','maritalStatus','jobIndustry','jobTitle','companyType',
                  'hasCar','hasHouse','isOnlyChild',)
        
        exclude = ('height','stateProvince','city', 'country', 'age', 'gender',  'photo','year_of_birth', 'month_of_birth', 'day_of_birth', 'ethnicGroup','bloodType',
        'hasChild' , 'link', 'streetAddress','position','language',
        'workStatus','companyName', 'educationCountry', 'educationSchool', 'isStudyAbroad',  
        'monthlyExpense', 'financialCondition', 'parentEducation', 
         'liveWithParent','likeChild',
         'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
         'belief','isSmoke','isDrink','beddingTime','pet','character',
            )