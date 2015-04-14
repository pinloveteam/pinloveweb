# -*- coding: utf-8 -*-
'''
Created on 2014年11月19日

@author: jin
'''
#个人基本详细
from django.forms.models import ModelForm
from apps.user_app.models import UserProfile
from django import forms
from django.forms.forms import Form
from apps.recommend_app.models import Grade
from django.core.validators import MaxValueValidator, MinValueValidator
EDUCATION_CHIOCES=((0,u'莫以读书论英雄（本科以下）'),(1,u'学历有限（大专）'),(2,u'十年寒窗（本科）'),(3,u'学有专攻（硕士)'),(4,u'才高八斗（博士'))
HEIGHT_CHIOCES=((185,u'鹤立鸡群（男大于1.85， 女大于1.75）'),(175,u' 玉树凌风（男大于1.75，女大于1.65）'),
                (170,u'俊秀挺拔（男大于1.7，女大于1.6）'),(160,u'及格线上（男大于1.6， 女1大于1.5）'),(155,u'短小精悍（男小于1.6， 女1小于1.5）'))
SCHOOL_CHIOCES=((4,u'如雷贯耳(985学校)'),(3,u'百年学府(重点学校)'),(2,u'中流砥柱(本科学校)'),(1,u'马马虎虎(专科学校)'),(0,u'布鲁弗莱（专科以下）'))

INCOME_CHIOCES=((99,u'钻石王老五(年薪>100w)'),(50,u'金领(年薪>50w)'),(30,u'蓝领(年薪>30w)'),(10,u'白领(年薪>10w)'),(5,u'无领白领(年薪>5w)'))
class InfoForm (ModelForm) : 
    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['education'].choices=EDUCATION_CHIOCES
        global HEIGHT_CHIOCES
        HEIGHT_CHIOCES_LIST=HEIGHT_CHIOCES
        if self.instance.gender=='F':
            HEIGHT_CHIOCES_LIST=[ (height[0]-5,height[1]) for height in HEIGHT_CHIOCES]
        self.fields['height'].choices=HEIGHT_CHIOCES_LIST
        self.fields['income'].choices=INCOME_CHIOCES
    schoolType=forms.TypedChoiceField(label=u"学校类型",choices=SCHOOL_CHIOCES)   
    class Meta : 
        model = UserProfile  
        fields = ( 'height',  'income','education',)
        
        exclude = ('stateProvince','avatar_name','city', 'country', 'age','sunSign', 'zodiac','avatar_name_status',
                   'self_evaluation','weight','hairStyle','hairColor','face','eyeColor','bodyShape',
                   'jobIndustry','jobTitle','companyType','workStatus','companyName','educationCountry','isStudyAbroad',
                   'belief','isSmoke','isDrink','beddingTime','pet','character',
                   'monthlyExpense','isOnlyChild','hasCar','hasHouse','financialCondition','parentEducation',
                   'liveWithParent','likeChild','lastLoginAddress', 'year_of_birth', 'month_of_birth', 'day_of_birth','ethnicGroup','bloodType',
         'maritalStatus', 'hasChild' ,'educationSchool','educationSchool', 'link', 'streetAddress','position','language',
                   ) 
        
        
class TaInfoForm(ModelForm) :
    def __init__(self, *args, **kwargs):
        super(TaInfoForm, self).__init__(*args, **kwargs)
        global HEIGHT_CHIOCES
        HEIGHT_CHIOCES_LIST=HEIGHT_CHIOCES
        if self.initial.get('gender')=='M':
            HEIGHT_CHIOCES_LIST=[ (height[0]-5,height[1]) for height in HEIGHT_CHIOCES]
            self.fields['expectHeight'].choices=HEIGHT_CHIOCES_LIST
        for field in ['heightweight','incomeweight','educationweight','characterweight']:
            self.fields[field].validators=[MinValueValidator(0), MaxValueValidator(100)]
    expectHeight=forms.ChoiceField(choices=HEIGHT_CHIOCES) 
        
    def cal_weight(self,userId):
        '''
        计算权重的值
        '''
        if Grade.objects.filter(user_id=userId).exists():
            grade=Grade.objects.get(user_id=userId)
        else:
            grade=Grade(user_id=userId)
        fieldList=['heightweight','incomeweight','educationweight','characterweight']
        sum,avg=0,0
        for field in fieldList:
            sum+=self.cleaned_data[field]
        avg=1.00/sum
        for field in fieldList:
            setattr( grade,field,avg*self.cleaned_data[field])
        grade.appearanceweight=0
        return grade
    
    def clean(self):
        sum=0
        for field in ['heightweight','incomeweight','educationweight','characterweight']:
            sum+=self.cleaned_data[field]
        if int(sum)==0:
            raise forms.ValidationError('权重不能全部为0!')
        return self.cleaned_data
        
    
    class Meta : 
        model = Grade  
        fields = ( 'heightweight',  'incomeweight','educationweight','characterweight')
   
    