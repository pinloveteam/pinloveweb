# -*- coding: utf-8 -*-

from django import forms

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
JOB_INDUSRY_CHOICE=((None,r'不限'),(0,r'IT|通信|电子|互联网'),(1,r'金融业'),(2,r'房地产|建筑业'),(3,r'商业服务'),(4,r'贸易|批发|零售|租赁业'),(5,r'问题教育|工体美术'),
                        (6,r'生产|加工|制造'),(8,r'交通|运输|物流仓库'),(9,r'服务业'),(10,r'文化|传媒|娱乐|体育'),
                        (11,r'能源|矿产|环保'),(12,r'政府|非盈利机构'),(13,r'农|林|牧|渔|其他'),
                        (14,r'在校学生'))

'''
搜索
'''
    
class SearchForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(SearchForm,self).__init__(*args,**kwargs)
        for key in self.fields:
            self.fields[key].required = False
        self.fields['minAge'].widget.attrs['class']='condition-input condition-input-pre'
        self.fields['maxAge'].widget.attrs['class']='condition-input condition-input-bak'
        self.fields['minHeigh'].widget.attrs['class']='condition-input condition-input-pre'
        self.fields['maxHeigh'].widget.attrs['class']='condition-input condition-input-bak'
        self.fields['education'].widget.attrs['class']='condition-input condition-input-pre'
        self.fields['minIcome'].widget.attrs['class']='condition-input condition-input-pre'
        self.fields['maxIncome'].widget.attrs['class']='condition-input condition-input-bak'
        self.fields['jobIndustry'].widget.attrs['class']='condition-input condition-input-pre'
    minAge=forms.ChoiceField(label="最小年龄",choices=MIN_AGE)
    maxAge=forms.ChoiceField(label="最大年龄",choices=MAX_AGE)
    education = forms.ChoiceField(label="学历",choices=EDUCATION_DEGREE_CHOICES)
    minIcome=forms.ChoiceField(label="最少年收入",choices=INCOME_CHOICES)
    maxIncome=forms.ChoiceField(label="最大年收入",choices=INCOME_CHOICES)
    minHeigh=forms.ChoiceField(label="最小身高",choices=HEIGHT_CHOICES)
    maxHeigh=forms.ChoiceField(label="最大身高",choices=HEIGHT_CHOICES)
    jobIndustry=forms.ChoiceField(label="行业",choices=JOB_INDUSRY_CHOICE,initial=None)
    
    