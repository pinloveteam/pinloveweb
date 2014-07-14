# -*- coding: utf-8 -*-
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from util.form_util import HorizRadioRenderer
import re
from django.core import validators
USERNAME_ERROR_MESSAGE=u'必填。英文，或者中文，或者下划线开头,2～20个字符'
class RegistrationForm (UserCreationForm) : 
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'     #添加css class 样式
        self.fields['username'].widget.attrs.update({'style' : 'width: 120px;'})
        self.fields['username'].widget.attrs['placeholder'] = r'请输入用户名'
        self.fields['password1'].widget.attrs['placeholder'] = r'请输入密码，6-20位字符，可由英文字母、数字和下划线组成'
        self.fields['password2'].widget.attrs['placeholder'] = r'再次输入密码'
    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(RegistrationForm, self).validate(value)
    email = forms.EmailField(required=True, label='邮件',widget=forms.TextInput(attrs={'placeholder': r'请输入常用邮箱'})) 
    gender=forms.ChoiceField(required=True, label='性别', choices=((u'M', u'帅哥'), (u'F', u'美女'), ),
                             widget=forms.RadioSelect())
    username=forms.RegexField(label=_("Username"), max_length=30,
        regex=ur'^[\u4e00-\u9fa5a-zA-Z\xa0-\xff_][\u4e00-\u9fa50-9a-zA-Z\xa0-\xff_]{1,19}$',
        help_text=USERNAME_ERROR_MESSAGE,
        error_messages={
            'invalid':USERNAME_ERROR_MESSAGE},
        validators=[
            validators.RegexValidator(re.compile(ur'^[\u4e00-\u9fa5a-zA-Z\xa0-\xff_][\u4e00-\u9fa50-9a-zA-Z\xa0-\xff_]{1,19}$'), USERNAME_ERROR_MESSAGE, 'invalid')]
                              )
    password1=forms.RegexField(label=_("Password"),widget=forms.PasswordInput,
        regex=r'^[0-9a-zA-Z\xff_]{6,20}$',
        help_text=r"必填。6-20位字符，可由英文字母、数字和下划线组成",
        error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'})
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
    
'''
修改密码
'''
class ChangePasswordForm(forms.Form): 
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'     #添加css class 样式
        self.fields['oldpassword'].widget.attrs['placeholder'] = r'请输入原密码'
        self.fields['newpassword'].widget.attrs['placeholder'] = r'6-20位字符，可由英文字母、数字和下划线组成'
        self.fields['newpassword1'].widget.attrs['placeholder'] = r'再次输入密码'
    oldpassword=forms.RegexField(label=_(u"原密码"),widget=forms.PasswordInput,regex=r'^[0-9a-zA-Z\xff_]{6,20}$', help_text=r"请输入原密码",error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'})
    newpassword=forms.RegexField(label=_(u"新密码"),widget=forms.PasswordInput,regex=r'^[0-9a-zA-Z\xff_]{6,20}$', help_text=r"6-20位字符，可由英文字母、数字和下划线组成",error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'})
    newpassword1=forms.RegexField(label=_(u"确认密码"),widget=forms.PasswordInput,regex=r'^[0-9a-zA-Z\xff_]{6,20}$', help_text=r"再次输入密码",error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'})
    
    error_messages={
                   'check_password_error':u'输入密码不相等!'
                   }
    def clean_newpassword1(self):
        newpassword=self.cleaned_data['newpassword']
        newpassword1=self.cleaned_data['newpassword1']
        if(newpassword!=newpassword1):
            raise forms.ValidationError(self.error_messages['check_password_error'])
