# -*- coding: utf-8 -*-

from django import forms
from apps.user_app.models import UserProfile
from pinloveweb import STAFF_MEMBERS

MIN_AGE=[(i,i) for i in range(18,60)]
MAX_AGE=[(i,i) for i in range(19,70)]
MAX_AGE.append((1000,'不限'))
EDUCATION_DEGREE_CHOICES=((-1,r'不限'),(0,r'大专以下'),(1,r'大专及以上'),(2,r'本科及以上'),(3,r'硕士及以上 '),(4,r'博士及以上 '),)
HEIGHT_CHOICES = ()
for height in range(130,226):  
        HEIGHT_CHOICES += ((height, str(height)),)
INCOME_CHOICES = ((-1,'不限'),(1,"5万以下"),)
for income in range(5,100,1):  
    INCOME_CHOICES += ((income, str(income)),)
INCOME_CHOICES += ((100000, "100万以上"),)
SUN_SIGN_CHOOSICE=((1,r'水瓶座'),(2,r'双鱼座'),(3,r'白羊座'),(4,r'金牛座'),(5,r'双子座'),(6,r'巨蟹座'),(7,r'狮子座'),(8,r'处女座'),(9,r'天秤座'),(10,r'天蝎座'),(11,r'射手座'),(12,r'摩羯座'),)
JOB_INDUSRY_CHOICE=((None,r'不限'),(0,r'IT|互联网'),(1,r'金融业'),(2,r'房地产|建筑业'),(3,r'商业服务'),(4,r'贸易|租赁'),(5,r'教育'),
                        (6,r'加工|制造'),(8,r'交通|物流'),(9,r'服务业'),(10,r'文化|传媒'),(11,r'能源|矿产'),
                        (12,r'政府|事业单位'),(13,r'农业'),(14,r'学生'),(15,r'通信|电子'),(16,r'批发|零售'),(17,r'科研'),
                        (18,r'体育'),(19,r'环保'),(20,r'非营利组织'),(21,r'农业'),(22,r'生物|制药'),(23,r'医疗|护理'),(24,r'其它'))

'''
搜索
'''
    
class SearchForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(SearchForm,self).__init__(*args,**kwargs)
        for key in self.fields:
            self.fields[key].required = False
            if key in ['minAge','minHeigh','education','minIcome','jobIndustry']:
                self.fields[key].widget.attrs['class']='condition-input condition-input-pre'
            elif key in ['maxAge','maxHeigh','maxIncome']:
                self.fields[key].widget.attrs['class']='condition-input condition-input-pre'
    minAge=forms.ChoiceField(label="最小年龄",choices=MIN_AGE)
    maxAge=forms.ChoiceField(label="最大年龄",choices=MAX_AGE)
    education = forms.ChoiceField(label="学历",choices=EDUCATION_DEGREE_CHOICES)
    minIcome=forms.ChoiceField(label="最少年收入",choices=INCOME_CHOICES)
    maxIncome=forms.ChoiceField(label="最大年收入",choices=INCOME_CHOICES)
    minHeigh=forms.ChoiceField(label="最小身高",choices=HEIGHT_CHOICES)
    maxHeigh=forms.ChoiceField(label="最大身高",choices=HEIGHT_CHOICES)
    jobIndustry=forms.ChoiceField(label="行业",choices=JOB_INDUSRY_CHOICE,initial=None)
    
    def init_search_condition(self,user_id):
        '''
初始化搜索条件
attribute：
   user_id 用户id
 
'''
        initial={}
        userProfile=UserProfile.objects.get(user_id=user_id)
        initial['isAvatar']=True
        initial['maxIncome']=-1
        initial['minIcome']=-1
        initial['jobIndustry']=None
        if userProfile.height==None:
            initial['minHeigh']=155
            initial['maxHeigh']=195
        if userProfile.age==None:
            initial['minAge']=18
            initial['maxAge']=30
        initial['education']=-1
        if userProfile.gender=='F':
            if  userProfile.height!=None:
                initial['minHeigh']=userProfile.height
                max=userProfile.height+30
                if max>226:
                    initial['maxHeigh']=226
                else:
                    initial['maxHeigh']=int(max)
            if userProfile.age!=None:
                initial['minAge']=int(userProfile.age)
                initial['maxAge']=int(userProfile.age+10)
        else:
            if userProfile.height!=None:
                initial['minHeigh']=int(userProfile.height-25)
                initial['maxHeigh']=int(userProfile.height)
            if userProfile.age!=None:
                initial['minAge']=int(userProfile.age-10)
                initial['maxAge']=int(userProfile.age)
        self.initial=initial
        
    def select_data(self,sunSign,gender,userId):
        '''
        查询搜索
        '''
        searchSql={}
        minAge=self.cleaned_data['minAge'] if self.cleaned_data['minAge']!=u'' else 0
        maxAge=self.cleaned_data['maxAge'] if self.cleaned_data['maxAge']!=u'' else 10000
        education=self.cleaned_data['education'] if self.cleaned_data['education'] !=u'' else -1
        minIcome=self.cleaned_data['minIcome'] if self.cleaned_data['minIcome']!=u'' else 0
        maxIncome=self.cleaned_data['maxIncome'] if self.cleaned_data['maxIncome'] !=u'' else 100000 
        #最大收入为不限
        if maxIncome=='-1':
            maxIncome='100000'
        minHeigh=self.cleaned_data['minHeigh'] if self.cleaned_data['minHeigh']!=u'' else 0
        maxHeigh=self.cleaned_data['maxHeigh'] if self.cleaned_data['maxHeigh']!=u'' else 1000
        if len(sunSign)>0:
            sunSign=[int(sunSignBean)for sunSignBean in sunSign.split(',')]
            searchSql['sunSign__in']=sunSign
        jobIndustry=self.cleaned_data['jobIndustry']
        if jobIndustry!='None' and jobIndustry!=u'':
            searchSql['jobIndustry']=jobIndustry
        if education=='0':
            searchSql['education']=education
        userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
                                    height__gte=minHeigh,height__lte=maxHeigh,**searchSql).exclude(gender=gender).exclude(user=userId).filter(avatar_name_status='3').exclude(user_id__in=STAFF_MEMBERS)[:80]
        return   userProfileList  
    
class SearchMobileForm(SearchForm):
    def __init__(self,*args,**kwargs):
        super(SearchMobileForm,self).__init__(*args,**kwargs)
        for key in self.fields:
            self.fields[key].required = False
            self.fields[key].widget.attrs['class']='form-control'
            