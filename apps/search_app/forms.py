# -*- coding: utf-8 -*-

from django import forms

MIN_AGE=[(i,i) for i in range(18,60)]
MAX_AGE=[(i,i) for i in range(19,70)]
MAX_AGE.append((1000,'不限'))
EDUCATION_DEGREE_CHOICES=((-1,r'不限'),(0,r'大专以下'),(1,r'大专及以上'),(2,r'本科及以上'),(3,r'硕士及以上 '),(4,r'博士及以上 '),)
HEIGHT_CHOICES = ()
for height in range(130,226):  
        HEIGHT_CHOICES += ((height, str(height)),)
INCOME_CHOICES = ((1,"5万以下"),)
for income in range(5,100,1):  
    INCOME_CHOICES += ((income, str(income)),)
INCOME_CHOICES += ((100000, "100万以上"),)
SUN_SIGN_CHOOSICE=((None,r'-----'),(1,r'水瓶座'),(2,r'双鱼座'),(3,r'白羊座'),(4,r'金牛座'),(5,r'双子座'),(6,r'巨蟹座'),(7,r'狮子座'),(8,r'处女座'),(9,r'天秤座'),(10,r'天蝎座'),(11,r'射手座'),(12,r'摩羯座'),)
JOB_INDUSRY_CHOICE=((None,r'-----'),(0,r'计算机/互联网/通信'),(1,r'公务员/事业单位'),(2,r'教师'),(3,r'医生'),(4,r'护士'),(5,r'空乘人员'),
                        (6,r'生产/工艺/制造'),(7,r'生产/工艺/制造'),(8,r'商业/服务业/个体经营'),(9,r'文化/广告/传媒'),(10,r'娱乐/艺术/表演'),
                        (11,r'律师/法务'),(12,r'教育/培训/管理咨询'),(13,r'建筑/房地产/物业'),(14,r'消费零售/贸易/交通物流'),(15,r'酒店旅游'),
                        (16,r'现代农业'),(17,r'在校学生'))
class AdvanceSearchForm(forms.Form):
    minAge=forms.ChoiceField(label="最小年龄",choices=MIN_AGE)
    maxAge=forms.ChoiceField(label="最大年龄",choices=MAX_AGE)
    education = forms.ChoiceField(label="学历",choices=EDUCATION_DEGREE_CHOICES)
    minIcome=forms.ChoiceField(label="最少年收入",choices=INCOME_CHOICES)
    maxIncome=forms.ChoiceField(label="最大年收入",choices=INCOME_CHOICES)
    minHeigh=forms.ChoiceField(label="最小身高",choices=HEIGHT_CHOICES)
    maxHeigh=forms.ChoiceField(label="最大身高",choices=HEIGHT_CHOICES)
    isAvatar=forms.BooleanField(label="是否 有头像",required=False)
    sunSign=forms.ChoiceField(label="星座",choices=SUN_SIGN_CHOOSICE)
    jobIndustry=forms.ChoiceField(label="行业",choices=JOB_INDUSRY_CHOICE)
    hasHouse=forms.ChoiceField(label="购房",choices=((None,'-----'),(True,r'是'),(False,r'否'),))
    hasCar=forms.ChoiceField(label="购车",choices=((None,'-----'),(True,r'是'),(False,r'否'),))
    stateProvince=forms.CharField(label="省份",max_length=50)
    country=forms.CharField(label="国家",max_length=50)
    city=forms.CharField(label="城市",max_length=50)

'''
简单搜索
'''
    
class SimpleSearchForm(forms.Form):
    minAge=forms.ChoiceField(label="最小年龄",choices=MIN_AGE)
    maxAge=forms.ChoiceField(label="最大年龄",choices=MAX_AGE)
    education = forms.ChoiceField(label="学历",choices=EDUCATION_DEGREE_CHOICES)
    minIcome=forms.ChoiceField(label="最少年收入",choices=INCOME_CHOICES)
    maxIncome=forms.ChoiceField(label="最大年收入",choices=INCOME_CHOICES)
    minHeigh=forms.ChoiceField(label="最小身高",choices=HEIGHT_CHOICES)
    maxHeigh=forms.ChoiceField(label="最大身高",choices=HEIGHT_CHOICES)
    isAvatar=forms.BooleanField(label="是否 有头像",required=False)
    
    