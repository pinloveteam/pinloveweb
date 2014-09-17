# -*- coding: utf-8 -*-
'''
Created on 2014年9月17日

@author: jin
'''
from django import forms 
import re
from django.core import validators
from django.contrib.auth.models import User
USERNAME_ERROR_MESSAGE=u'必填。英文，1-14位字符，英文字母、数字和下划线组成或中文7个字符'
class ConfirmInfo(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConfirmInfo, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'     #添加css class 样式
        self.fields['username'].widget.attrs['placeholder'] = r'请输入用户名,1-14位字符，英文字母、数字和下划线组成或中文7个字符'

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(ConfirmInfo, self).validate(value)
    gender=forms.ChoiceField(required=True, label='性别', choices=((u'M', u'男'), (u'F', u'女'), ),
                             widget=forms.RadioSelect())
    USERNAME_LENGTH_LIMIT=14
    username=forms.RegexField(label="Username", max_length=30,
        regex=ur'^[\u4e00-\u9fa5a-zA-Z\xa0-\xff_][\u4e00-\u9fa50-9a-zA-Z\xa0-\xff_]{1,19}$',
        help_text=USERNAME_ERROR_MESSAGE,
        error_messages={
            'invalid':USERNAME_ERROR_MESSAGE},
        validators=[
            validators.RegexValidator(re.compile(ur'^[\u4e00-\u9fa5a-zA-Z\xa0-\xff_][\u4e00-\u9fa50-9a-zA-Z\xa0-\xff_]{1,19}$'), USERNAME_ERROR_MESSAGE, 'invalid')]
                              )
    error_messages = {
        'duplicate_email':r'邮件已被注册!',
        'duplicate_username': u'该用户已经存在',
        'too_long_username':r'用户名长度超标!',
    }
        
    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise forms.ValidationError(self.error_messages['duplicate_username'])
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        if len(username.encode('gbk'))>self.USERNAME_LENGTH_LIMIT:
            raise forms.ValidationError(self.error_messages['too_long_username'])
        return username
            