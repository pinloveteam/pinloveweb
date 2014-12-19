#-*- coding: UTF-8 -*- 
from apps.user_app.models import UserProfile
import logging
from django.shortcuts import render
from apps.recommend_app.models import Grade
logger=logging.getLogger(__name__)

def account(request):
    '''
    获得账户信息
    '''
    args={}
    try:
        userProfile=UserProfile.objects.get(user=request.user) 
        args['avatar_name']=userProfile.avatar_name
        from apps.pay_app.method import get_charge_amount
        args['pinLoveIcon']=get_charge_amount(userId=request.user)
        return render(request,'mobile_account.html',args)
    except Exception as e:
        logger.exception('手机获取账户信息出错：'+e.message)
        args={'result':'error','error_message':e.message}
        return render(request,'error.html',args)
        
        
def get_weight(request,template_name):
    '''
    获取用户权重
    '''
    args={}
    try:
        grade=Grade.objects.filter(user_id=request.user.id)
        if len(grade)==0:
            for field in ['heightweight','incomeweight','educationweight','appearanceweight','characterweight']:
                args[field]=0
        else:
            for field in ['heightweight','incomeweight','educationweight','appearanceweight','characterweight']:
                value=getattr(grade[0],field)
                if value==None:
                    value=0;
                args[field]=int(value*100)
    except Exception as e:
         logger.exception(e.message)
         return render()