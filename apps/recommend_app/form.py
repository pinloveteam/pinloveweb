# -*- coding: utf-8 -*-
'''
Created on Sep 18, 2013

@author: jin
'''
from apps.recommend_app.models import Grade, UserExpect, WeightStar
from django.forms.models import ModelForm
from django.forms import forms
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
        
        

    