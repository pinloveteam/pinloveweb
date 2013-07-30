# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm (UserCreationForm) : 
    
    email = forms.EmailField(required=True, label='邮件') 
    
    # my_default_errors = { 'required': u'此项信息必须',
    #'invalid': u'请输入正确的数值'}
    
    #def __init__(self, *args, **kwargs) : 
    #    super(RegistrationForm, self).__init__(*args, **kwargs)
    #    self.error_messages['email'] = '错误的邮件地址'
    error_messages = {
        'duplicate_email': ("邮件已存在！")
    }
            
    class Meta : 
        model = User 
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    # def save(self, commit=True) : 
    #    user = super(UserCreationForm,self).save(commit=False)
    #    user.email = self.cleaned_data['email']

    #    if commit : 
    #        user.save() 

    #    return user 