# -*- coding: utf-8 -*-
'''
Created on Sep 18, 2013

@author: jin
'''
from apps.recommend_app.models import Grade, UserExpect
from django.forms.models import ModelForm
"""
  权重
"""
class WeightForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeightForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            #每一个属性不是必填的
            self.fields[key].required = False
    class Meta:
        model=Grade
        fields=('heightweight','incomeweight','edcationweight','appearanceweight' ,'characterweight',)
        exclude =('heightscore','incomescore','edcationscore','appearancescore','appearancesvote',)
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
        
        

    