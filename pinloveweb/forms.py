# -*- coding: utf-8 -*-
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
import re
from django.core import validators
from django.core.cache import cache
from django.core.files.uploadhandler import FileUploadHandler
from apps.user_app.models import UserProfile
import datetime
USERNAME_ERROR_MESSAGE=u'必填。英文，1-14位字符，英文字母、数字和下划线组成或中文7个字符'
class RegistrationForm (UserCreationForm) : 
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'     #添加css class 样式
        self.fields['username'].widget.attrs['placeholder'] = r'请输入用户名,9位字符，中英字母、数字和下划线组成'
        self.fields['password1'].widget.attrs['placeholder'] = r'请输入密码，6-20位字符，可由英文字母、数字和下划线组成'
        self.fields['password2'].widget.attrs['placeholder'] = r'再次输入密码'
        #字段必须的错误提示改为中文
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname}必须要填!'.format(
                fieldname=unicode(field.label))}
            
    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(RegistrationForm, self).validate(value)
    email = forms.EmailField(required=True, label='邮件',widget=forms.TextInput(attrs={'placeholder': r'请输入常用邮箱'})) 
    gender=forms.ChoiceField(required=True, label='性别', choices=((u'M', u'男'), (u'F', u'女'), ),
                             widget=forms.RadioSelect())
    USERNAME_LENGTH_LIMIT=14
    username=forms.RegexField(label=_("Username"), max_length=30,
        regex=ur'^[\u4e00-\u9fa5a-zA-Z\xa0-\xff_][\u4e00-\u9fa50-9a-zA-Z\xa0-\xff_\s]{1,9}$',
        help_text=USERNAME_ERROR_MESSAGE,
        error_messages={
            'invalid':USERNAME_ERROR_MESSAGE},
        validators=[
            validators.RegexValidator(re.compile(ur'^[\u4e00-\u9fa5a-zA-Z\xa0-\xff_][\u4e00-\u9fa50-9a-zA-Z\xa0-\xff_\s]{1,19}$'), USERNAME_ERROR_MESSAGE, 'invalid')]
                              )
    password1=forms.RegexField(label=_("Password"),widget=forms.PasswordInput,
        regex=r'^[0-9a-zA-Z\xff_]{6,20}$',
        help_text=r"必填。6-20位字符，可由英文字母、数字和下划线组成",
        error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'})
    
    year_of_birth=forms.ChoiceField(label="出生年" ,choices=[(-1,'生日-年'),]+[(temp[0],'%s年'%(temp[1])) for temp in UserProfile.YEAR_OF_BIRTH_CHOICES[1:] ])
    month_of_birth=forms.ChoiceField(label="出生月" ,choices=[(-1,'月'),]+[(temp[0],'%s月'%(temp[1])) for temp in UserProfile.MONTH_OF_BIRTH_CHOICES[1:] ])
    day_of_birth=forms.ChoiceField(label="出生日" ,choices=[(-1,'日'),]+list(UserProfile.DAY_OF_BIRTH_CHOICES[:1])+[(temp[0],'%s日'%(temp[1])) for temp in UserProfile.DAY_OF_BIRTH_CHOICES[1:] ])
    
    def clean_day_of_birth(self):
        day_of_birth=self.cleaned_data['day_of_birth']
        month_of_birth=self.cleaned_data['month_of_birth']
        year_of_birth=self.cleaned_data['year_of_birth']
        if not((day_of_birth==-1 and month_of_birth==-1 and year_of_birth==-1) or (day_of_birth!=-1 and month_of_birth!=-1 and year_of_birth!=-1)):
            raise  forms.ValidationError(u'请正确填写出生日期!')
        try:
            datetime.date(int(year_of_birth),int(month_of_birth),int(day_of_birth))
        except Exception as e:
            raise  forms.ValidationError(u'请填写有效的出生日期!')
        return day_of_birth
    
    # my_default_errors = { 'required': u'此项信息必须',
    #'invalid': u'请输入正确的数值'}
    
    #def __init__(self, *args, **kwargs) : 
    #    super(RegistrationForm, self).__init__(*args, **kwargs)
    #    self.error_messages['email'] = '错误的邮件地址'
    error_messages = {
        'duplicate_email':r'邮件已被注册!',
        'duplicate_username': _("A user with that username already exists."),
        'too_long_username':r'用户名长度超标!',
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
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
#         username = self.cleaned_data["username"]
#         if len(username.encode('gbk'))>self.USERNAME_LENGTH_LIMIT:
#             raise forms.ValidationError(self.error_messages['too_long_username'])
#         return username
#         try:
#             User._default_manager.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError(self.error_messages['duplicate_username'])


    
'''
重置密码
newpassword 新密码
newpassword1 新密码验证
'''
class ResetPasswordForm(forms.Form): 
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'     #添加css class 样式
        self.fields['newpassword'].widget.attrs['placeholder'] = r'6-20位字符，可由英文字母、数字和下划线组成'
        self.fields['newpassword1'].widget.attrs['placeholder'] = r'再次输入密码'
        
    newpassword=forms.RegexField(label=_(u"新密码"),widget=forms.PasswordInput,regex=r'^[0-9a-zA-Z\xff_]{6,20}$', help_text=r"6-20位字符，可由英文字母、数字和下划线组成",error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'},required=True)
    newpassword1=forms.RegexField(label=_(u"确认密码"),widget=forms.PasswordInput,regex=r'^[0-9a-zA-Z\xff_]{6,20}$', help_text=r"再次输入密码",error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'},required=True)
    
    error_messages={
                   'check_password_error':u'输入密码不相等!',
                   'password_incorrect':u'原密码错误!',
                   }
    
    def clean_newpassword1(self):
        newpassword=self.cleaned_data['newpassword']
        newpassword1=self.cleaned_data['newpassword1']
        if(newpassword!=newpassword1):
            raise forms.ValidationError(self.error_messages['check_password_error'])
        return newpassword1
'''
修改密码
oldpassword 旧密码
'''   
class ChangePasswordForm(ResetPasswordForm): 
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'     #添加css class 样式
        self.fields['oldpassword'].widget.attrs['placeholder'] = r'请输入原密码'
        
    oldpassword=forms.RegexField(label=_(u"原密码"),widget=forms.PasswordInput,regex=r'^[0-9a-zA-Z\xff_]{6,20}$', help_text=r"请输入原密码",error_messages={
            'invalid':r'必须由英文字母、数字和下划线组成,6-20个字符'},required=True)
     
   
'''
进度条
'''
class UploadProgressCachedHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, 'X-Progress-ID'
    which should contain a unique string to identify the upload to be tracked.
    """

    def __init__(self, request=None):
        super(UploadProgressCachedHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET :
            self.progress_id = self.request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in self.request.META:
            self.progress_id = self.request.META['X-Progress-ID']
        if self.progress_id:
            self.cache_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], self.progress_id )
            cache.set(self.cache_key, {
                'length': self.content_length,
                'uploaded' : 0
            })

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        if self.cache_key:
            data = cache.get(self.cache_key)
            data['uploaded'] += self.chunk_size
            cache.set(self.cache_key, data)
        return raw_data
    
    def file_complete(self, file_size):
        pass

    def upload_complete(self):
        if self.cache_key:
            cache.delete(self.cache_key)
