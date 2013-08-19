# -*- coding: utf-8 -*-
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from util.form_util import HorizRadioRenderer

class RegistrationForm (UserCreationForm) : 
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'input-xlarge'     #添加css class 样式
        self.fields['username'].widget.attrs['placeholder'] = r'请输入用户名'
        self.fields['password1'].widget.attrs['placeholder'] = r'6-16个字符组成，不能为9为以下纯数字'
        self.fields['password2'].widget.attrs['placeholder'] = r'再次输入密码'
         
    email = forms.EmailField(required=True, label='邮件',widget=forms.TextInput(attrs={'placeholder': r'请输入常用邮箱'})) 
    gender=forms.ChoiceField(required=True, label='性别', choices=((u'M', u'帅哥'), (u'F', u'美女'), ),
                             widget=forms.RadioSelect())
    # my_default_errors = { 'required': u'此项信息必须',
    #'invalid': u'请输入正确的数值'}
    
    #def __init__(self, *args, **kwargs) : 
    #    super(RegistrationForm, self).__init__(*args, **kwargs)
    #    self.error_messages['email'] = '错误的邮件地址'
    error_messages = {
        'duplicate_email':r'邮件已被注册!',
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
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
#     def clean_username(self):
#         # Since User.username is unique, this check is redundant,
#         # but it sets a nicer error message than the ORM. See #13147.
#         username = self.cleaned_data["username"]
#         try:
#             User._default_manager.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError(self.error_messages['duplicate_username'])

    # def save(self, commit=True) : 
    #    user = super(UserCreationForm,self).save(commit=False)
    #    user.email = self.cleaned_data['email']

    #    if commit : 
    #        user.save() 

    #    return user 