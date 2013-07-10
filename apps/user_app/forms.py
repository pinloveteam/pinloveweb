# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm

from apps.user_app.models import User_Profile

class UserProfileForm (ModelForm) : 
#     stateProvince=forms.ChoiceField(label=r"所在省",)
#     city=forms.ChoiceField(label=r"所在城市",)
#     streetAddress=forms.ChoiceField(label=r"街道地址",)
    class Meta : 
        model = User_Profile  
        fields = ('trueName', 'gender', 'myPhoto','year_of_birth', 'month_of_birth', 'day_of_birth', 'height', 'maritalStatus', 
        'country',   'link',
        'mobilePhone', 'jobIndustry', 'jobTitle', 'income', 'educationDegree', 'educationCountry', 'educationSchool', 
        'interests', 'selfEvaluation', 
        )
        exclude = ('stateProvince','city', 'streetAddress','age') 
    
       