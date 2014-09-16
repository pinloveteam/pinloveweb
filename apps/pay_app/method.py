# -*- coding: utf-8 -*-
'''
Created on 2014年5月27日

@author: jin
'''
from apps.pay_app.models import ChargeExchangeRelate, Charge, ChargeDetail
from django.db import transaction
import datetime
'''
使用拼爱币查看对方分数
'''
def use_charge_by_other_score(myId,otherId):
    #判断是否有金额
    if has_PLprice(myId,'1002'):
        #扣除所需拼爱币
        charge_save(myId,'1002',)
        #被看的人获得拼爱币
        charge_save(otherId,'1003',)
        return 'success'
    else:
        return 'less'

'''
检查积分拼爱币是否足够支付
@param userId:用户id
@param type:支付类型 (pintu|)
@return: args
'''
def check_score_and_PLprice(userId,type):
    from apps.pay_app.pay_settings import SCORE_PLPRICE_TYPE
    type=SCORE_PLPRICE_TYPE[type]
    args={}
    from apps.user_score_app.method import has_score_by_pintu
    hasScore=has_score_by_pintu(userId)
    if hasScore:
        from apps.user_score_app.models import UserScoreExchangeRelate
        userScoreExchangeRelate=UserScoreExchangeRelate.objects.get(type=type['score'])
        args={'type':'score','amount':userScoreExchangeRelate.amount,}
    else:
        hasCharge=has_charge_by_pintu(userId)
        if hasCharge:
            chargeExchangeRelate=ChargeExchangeRelate.objects.get(operateType=type['charge'])
            args={'type':'charge','amount':chargeExchangeRelate.PLPrice}
        else:
            args={'type':'less'}
    return args

'''
扣除玩一次缘分拼图的拼爱币
'''   
def use_charge_by_pintu(userId):
    return charge_save(userId,'1004')
'''
是否可玩缘分拼图
''' 
def has_charge_by_pintu(userId):
    return has_PLprice(userId,'1004')
'''
账户内的拼爱币是否可支付消费
attribute：
     userId： 用户id
     type:   消费类型
'''   
def has_PLprice(userId,type,*args,**kwargs):
    chargeExchangeRelate=ChargeExchangeRelate.objects.get(operateType=type)
    charge=Charge.objects.get(user_id=userId)
    if chargeExchangeRelate.PLPrice+charge.validAmount<0:
        return False
    else:
        return True
'''
拼爱币修改操作
attridute:
    userId 用户id
    type   拼爱币操作类型
    **kwargs：data(option)  说明
return:
    less 消耗积分超过剩余有效拼爱币
    success 积分修改成功
'''
@transaction.commit_on_success    
def charge_save(userId,type,*args,**kwargs):
    chargeExchangeRelate=ChargeExchangeRelate.objects.get(operateType=type)
    charge=Charge.objects.get(user_id=userId)
    charge.validAmount+=chargeExchangeRelate.PLPrice
    time=datetime.datetime.today()
    data=kwargs.get('data',False)
    if not data:
        data=chargeExchangeRelate.instruction
    ChargeDetail(user_id=userId,amount=chargeExchangeRelate.PLPrice,data=data,time=time,type=type).save()
    charge.save()

'''
获得有效拼爱币的数量
'''
def get_charge_vailAmount(userId):
    return Charge.objects.get(user_id=userId).validAmount

'''
获得拼爱币数量(有效+赠送)
@param userId: 用户id
option：
@param vailPinLoveIcon:有效拼爱币 
@param freePinLoveIcon:免费拼爱币 
'''
def get_charge_amount(userId,**kwargs):
    from apps.user_score_app.method import get_valid_score
    if kwargs.get('vailPinLoveIcon',None)!=None:
         return get_valid_score(userId)+kwargs.get('vailPinLoveIcon')
    elif kwargs.get('freePinLoveIcon',None)!=None:
        vailPinLoveIcon=Charge.objects.get(user_id=userId).validAmount
        return kwargs.get('freePinLoveIcon')+vailPinLoveIcon
    else:
        vailPinLoveIcon=Charge.objects.get(user_id=userId).validAmount
        return get_valid_score(userId)+vailPinLoveIcon
   