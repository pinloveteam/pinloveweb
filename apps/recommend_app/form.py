# -*- coding: utf-8 -*-
'''
Created on Sep 18, 2013

@author: jin
'''
from apps.recommend_app.models import Grade, UserExpect, WeightStar
from django.forms.models import ModelForm
from django.forms import forms
from django.core.validators import MaxValueValidator, MinValueValidator
"""
权重对应的星星
"""
class StartForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            #每一个属性不是必填的
            self.fields[key].required = False
            if self.fields[key].initial is None:self.fields[key].initial=0
    def clean(self):
        sum,flag=0,True
        for key,value in self.cleaned_data.items():
            if value>5:
                raise forms.ValidationError(u'参数错误,星星数不得大于5!')
            elif value<0:
                raise forms.ValidationError(u'参数错误,星星数不得小于0')
            sum=+value
        if sum==0:
            raise forms.ValidationError(u'权重不能为空!')
        return self.cleaned_data
    class Meta:
        model=WeightStar
        exclude=('user')
"""
  对另一半打分
"""   
class GradeForOther(ModelForm): 
#     def __init__(self, *args, **kwargs):
#         super(WeightForm, self).__init__(*args, **kwargs)
#         for key in self.fields:
#             #每一个属性不是必填的
#             self.fields[key].required = False
    class Meta:
        model=UserExpect
        fields=('heighty1','heighty2','heighty3','heighty4','heighty5','heighty6','heighty7','heighty8',)
        exclude=()
        
    
class WeightForm(ModelForm) :
    __FEILD_LIST=['heightweight','incomeweight','educationweight','characterweight','appearanceweight']
    def __init__(self, *args, **kwargs):
        super(WeightForm, self).__init__(*args, **kwargs)
        for field in self.__FEILD_LIST:
            self.fields[field].validators=[MinValueValidator(0), MaxValueValidator(100)]
        
    def cal_weight(self,userId):
        '''
        计算权重的值
        '''
        if Grade.objects.filter(user_id=userId).exists():
            grade=Grade.objects.get(user_id=userId)
        else:
            grade=Grade(user_id=userId)
        fieldList=self.__FEILD_LIST
        sum,avg=0,0
        for field in fieldList:
            sum+=self.cleaned_data[field]
        avg=1.00/sum
        for field in fieldList:
            
            setattr( grade,field,avg*self.cleaned_data[field])
        #保存权重数值
        weightList=['height','income','education','character','appearance']
        if WeightStar.objects.filter(user_id=userId).exists():
            weightStar=WeightStar.objects.get(user=userId)
        else:
            weightStar=WeightStar(user_id=userId)
        for weight in weightList:
            setattr( weightStar,weight,self.cleaned_data[weight+'weight'])
        weightStar.save()
        return grade
    
    def clean(self):
        sum=0
        for field in self.__FEILD_LIST:
            sum+=self.cleaned_data[field]
        if int(sum)==0:
            raise forms.ValidationError('权重不能全部为0!')
        return self.cleaned_data
        
    
    class Meta : 
        model = Grade  
        fields =('heightweight','incomeweight','educationweight','characterweight','appearanceweight')

    