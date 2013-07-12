# -*- coding: utf-8 -*-
'''
Created on 2013-6-27

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
class User_Profile(models.Model):
    
    user = models.ForeignKey(User)
    # email=models.EmailField(max_length=128)
    
    # basic information 
    trueName = models.CharField(verbose_name=r"真实姓名", max_length=50)
    
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ( (MALE, r'男'), (FEMALE, r'女'), )
    gender = models.CharField(verbose_name=r"性别", max_length=1, choices=GENDER_CHOICES, default=MALE) # sex=models.CharField(max_length=1) 
    
    YEAR_OF_BIRTH_CHOICES = ()
    for year in range(1900,2013):  
        YEAR_OF_BIRTH_CHOICES += ((year, str(year)),)
    year_of_birth = models.SmallIntegerField(verbose_name=r"出生年份", choices=YEAR_OF_BIRTH_CHOICES, default=1985) 

    MONTH_OF_BIRTH_CHOICES = ()
    for month in range(1,13):  
        MONTH_OF_BIRTH_CHOICES += ((month, str(month)),)
    month_of_birth = models.SmallIntegerField(verbose_name=r"出生月份", choices=MONTH_OF_BIRTH_CHOICES, default=1)  
    
    DAY_OF_BIRTH_CHOICES = ()
    for day in range(1,32):  
        DAY_OF_BIRTH_CHOICES += ((day, str(day)),)
    day_of_birth = models.SmallIntegerField(verbose_name=r"出生日期", choices=DAY_OF_BIRTH_CHOICES, default=1)
    age = models.IntegerField(max_length=50)
    # day_of_birth = models.SmallIntegerField()  # age = models.SmallIntegerField() # age=models.IntegerField(max_length=8)
    # birthday = models.DateField(verbose_name=r"生日", auto_now=False, auto_now_add=False, widget=forms.DateInput)
    HEIGHT_CHOICES = ()
    for height in range(130,226):  
        HEIGHT_CHOICES += ((height, str(height)),)
    height = models.IntegerField(verbose_name=r"身高（厘米）", choices=HEIGHT_CHOICES, default=170)  # height=models.IntegerField(max_length=8) 
    
    SINGLE = 'S'
    MARRIED = 'M'
    DIVORCED = 'D'
    WIDOWED = 'W'
    SEPARATED = 'SE'
    MARITAL_STATUS_CHOICES = ( (SINGLE, r'单身'), (MARRIED, r'已婚'), (DIVORCED, r'离婚'), (SEPARATED, r'分居'), (WIDOWED, r'丧偶'))
    maritalStatus = models.CharField(verbose_name=r"婚姻状态", max_length=1, choices=MARITAL_STATUS_CHOICES, default=SINGLE)  # single - 0, married - 1, separated - 2, divorced - 3, widowed - 4 # marriageState=models.CharField(max_length=1)
    
    # personal web and links 
    link=models.CharField(verbose_name=r"共享链接",max_length=128,default='me')  
#     facebookLink = models.URLField(verbose_name=r"Facebook链接", default="http://www.facebook.com/me")
#     linkedInLink = models.URLField(verbose_name=r"LinkedIn链接", default="http://www.linkedin.com/me")
#     weiboLink = models.URLField(verbose_name=r"微博链接", default="http://www.weibo.com/me")
#     renrenLink = models.URLField(verbose_name=r"人人网链接", default="http://www.renren.com/me") 
    
    # location
    COUNTRY_CHOICES = (('CN', r'中国'), ('US', r'美国'))
    country = models.CharField(verbose_name=r"所在国家", max_length=2, choices=COUNTRY_CHOICES, default='CN')
    stateProvince = models.CharField(verbose_name=r"所在省", max_length=50) 
    
    city = models.CharField(verbose_name=r"所在城市", max_length=50) 
    streetAddress = models.CharField(verbose_name=r"街道地址", max_length=255) # address = models.CharField(max_length=255)
    
    # phone number 
    mobilePhone = models.CharField(verbose_name=r"电话号码", max_length=50)
    
    # current job 
    jobIndustry = models.CharField(verbose_name=r"职业领域", max_length=50) # job = models.CharField(max_length=50)
    jobTitle = models.CharField(verbose_name=r"职业", max_length=50) # position = models.CharField(max_length=50)
    
    INCOME_CHOICES = ()
    for income in range(0,50,1):  
        INCOME_CHOICES += ((income, str(income)),)
    income = models.IntegerField(verbose_name=r"年薪（万元）", choices=INCOME_CHOICES, default=0) # payRang=models.CharField(max_length=50)
    
    # previous working experience
    
    # education experience 
    educationDegree = models.CharField(verbose_name=r"最高学位", max_length=50) # educate = models.CharField(max_length=50)
    educationCountry = models.CharField(verbose_name=r"最高学位毕业国家", max_length=50) 
    educationSchool = models.CharField(verbose_name=r"最高学位毕业学校", max_length=100) # educate = models.CharField(max_length=50)
    
    # previous education experience 
    
    interests = models.TextField(verbose_name=r"个人爱好", max_length=50) # hobby = models.CharField(default = '',max_length=255) 
    selfEvaluation = models.TextField(verbose_name=r"个人自我评价", max_length=50) # evaluate=models.TextField(default = '')

    # photo, audio, vedio 
    myPhoto = models.ImageField(verbose_name=r"头像",upload_to='user_img',max_length=128,default='')
    # myVoice = models.FileField()
    # myVideo = models.FileField()
   
    # pinlove verification 
    # verificationStatus = models.IntegerField() # bit 0 : self verified - self_verified
                                               # bit 1 : verified by website - web_verified
                                               # bit 2 : verified by friends or families - family_friend_verified
                                               # bit 3 : verified by pinlove team - pinlove_verified   
    
    # login status 
    # lastLoginTime = models.DateField(auto_now=False,auto_now_add=False)
    
    # checkState=models.CharField(max_length=1)
    # stauts=models.CharField(max_length=1)    
    
class Friend(models.Model):
    myId=models.ForeignKey(User,related_name='user_myId')
    friendId=models.ForeignKey(User,related_name='user_friendId')
    # friend type
    type=models.CharField(max_length=1)
#     
# class Message(models.Model):
#     messageId=models.AutoField(primary_key=True,max_length=8)
#     fromId=models.ForeignKey(User,related_name='User_fromId')
#     toId=models.ForeignKey(User,related_name='User_toId')
#     messageContent=models.TextField()
#     sendTime=models.DateTimeField()
#     type=models.CharField(max_length=1)
#     
# class New(models.Model):
#     newId=models.AutoField(primary_key=True,max_length=8)
#     userId=models.ForeignKey(User,related_name='User_userId')
#     createTime=models.DateTimeField()
#     contentText=models.CharField(max_length=255)
#     picture_path=models.ImageField(upload_to='news_img',max_length=128)
#     video_path=models.CharField(max_length=128)
#     commentNum=models.IntegerField(default=0)
#     shareNum=models.IntegerField(default=0)
#     type=models.CharField(max_length=1)

class Dictionary(models.Model):

    key=models.CharField(max_length=128)
    name=models.CharField(max_length=255,default='')
    value=models.CharField(max_length=255)