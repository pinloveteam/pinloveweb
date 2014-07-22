# -*- coding: utf-8 -*-
'''
Created on Sep 8, 2013

@author: jin
'''
from django.shortcuts import render
from apps.pay_app.models import FacebookPayDetail, ChargeExchangeRelate, Charge,\
    Order
from django.utils import simplejson
from django.http.response import HttpResponse, HttpResponseRedirect
import logging
from django.views.decorators.csrf import csrf_exempt
from apps.user_app.models import UserProfile
from django.db import transaction
from util.page import page
logger=logging.getLogger(__name__)
##############
###1.0

def get_icon(request):
    return render(request,'icon.html')

'''
facebook 交易结果记录
'''
def pay_detail(request):
    args={}
    data=request.REQUEST.get('data',False)
    data=simplejson.loads(data)
    uid=request.session['uid']
    if data:
        paymentId=data['payment_id']
        amount=float(data['amount'])
        currency=data['currency']
        quantity=int(data['quantity'])
        signed_request=data['signed_request']
        status=data['status']
        FacebookPayDetail(id=paymentId,amount=amount,currency=currency,quantity=quantity,status=status,signed_request=signed_request).save()
        if status=='completed':
            from apps.game_app.models import get_game_count_forever,set_game_count_forever
            set_game_count_forever(uid,get_game_count_forever(uid)+quantity)
        args['result']='success'
        from apps.game_app.models import get_count
        args['game_count']=get_count(uid)+get_game_count_forever(uid)
    else:
        args['result']='error'
    json=simplejson.dumps(args)
    return HttpResponse(json)

'''
会员购买页面
'''
@csrf_exempt
def member(request):
    try:
        args={}
        userProfile=UserProfile.objects.get(user=request.user)
        #获取城市代码
        from util.location import get_country_code
        countryCode=get_country_code(request)
        if countryCode=='US':
            chargeExchangeRelateList=ChargeExchangeRelate.objects.filter(currencyType=1)
        elif countryCode=='CN':
            chargeExchangeRelateList=ChargeExchangeRelate.objects.filter(currencyType=2)
        else:
            chargeExchangeRelateList=ChargeExchangeRelate.objects.filter(currencyType=2)
        charge=Charge.objects.get(user_id=request.user.id)
        args['chargeExchangeRelateList']=chargeExchangeRelateList
        args['charge']=charge
        #初始化个人信息模块
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        from pinloveweb.method import get_no_read_web_count
        args.update(get_no_read_web_count(request.user.id))
        return render(request,'buy.html',args)
    except Exception as e:
        errorMessage='会员购买页面出错'
        logger.exception('%s%s%s' %(errorMessage,'出错原因:',e))
        return render(request,'buy.html',{'errorMessage':errorMessage})

#===============================
#下订单，并跳转到第三方制度
#===============================
def pay_icon_order(request):
    args={}
    try:
       if request.method=="POST":
           id=int(request.REQUEST.get('id',False))
           type=request.REQUEST.get('type',False)
           chargeExchangeRelate=ChargeExchangeRelate.objects.get(id=id)
           if type=='paypal':
#                args['type']='paypal'
               from apps.pay_app.PayPal import asks_for_money
               args=asks_for_money(userId=request.user.id,amount=chargeExchangeRelate.get_amount(),price=chargeExchangeRelate.currencyPrice,currency=chargeExchangeRelate.currencyType,data=u'购买拼爱币')
           elif type=='alipay':
               from apps.alipay_app.alipay import build_aplipay_order
               args=build_aplipay_order(userId=request.user.id,amount=chargeExchangeRelate.get_amount(),price=chargeExchangeRelate.currencyPrice,currency=chargeExchangeRelate.currencyType,data=u'购买拼爱币')
               logger.error('args====')
           return render(request,'redirect_to_pay.html',args)
       else:
            return HttpResponseRedirect('/pay/member/')
    except Exception as e:
        print e
    
@transaction.commit_on_success          
def redeem_price(request):
    try:
        args={}
        validAmount=int(request.REQUEST.get('validAmount',False))
        type=request.REQUEST.get('type',False)
        if not(validAmount and validAmount):
            raise Exception('缺少参数!')
        charge=Charge.objects.get(user_id=request.user.id)
        if charge.validAmount>=validAmount:
            order=Order(user_id=request.user.id,amount=validAmount,price=(validAmount+0.00)/100,status='initiated',type='1',pattern='2')
            order.data=order.get_pattern_display()
            order.get_order_id(request.user.id)
            if type==u'alipay':
                order.channel='1'
                order.currency='RMB'
            elif type==u'paypal':
                order.channel='2'
                order.currency='USB'
            order.save()
            charge.validAmount=charge.validAmount-validAmount
            charge.freezeAmount=charge.freezeAmount+validAmount
            charge.save()
            args={'result':'success','message':u'提交成功等待审核!'} 
        elif validAmount>0:
            args={'result':'error','error_message':u'金额不足'}
        else:
             args={'result':'error','error_message':u'输入金额不能为负'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception as e:
        print e
    
'''
交易记录
'''    
def charge_record(request):   
    args={} 
    sql='''
    SELECT *   from `order` u
where u.user_id=%s and not(u.`status`='initial' and u.channel='1' and u.updateTime is null)
ORDER BY IF(u.createTime>IFNULL(u.updateTime,DATE(0)),u.createTime,u.updateTime) DESC

    '''
    orderList=Order.objects.raw(sql,[request.user.id])
    data=page(request,orderList,page_num=8)
    args['has_next']=data['pages'].has_next()
    if data['pages'].has_next():
        args['next_page_number']=data['pages'].next_page_number()
    if data['pages'].has_previous():
        args['previous_page_number']=data['pages'].previous_page_number()
    args['has_previous']=data['pages'].has_previous()
    list=[]
    for order in data['pages'].object_list:
        dict={}
        dict['amount']=order.amount
        dict['data']=order.data
        if order.updateTime!=None:
            dict['time']=order.updateTime.strftime("%Y-%m-%d")
        else:
             dict['time']=order.createTime.strftime("%Y-%m-%d")
        dict['channel']=order.get_channel_display()
        dict['type']=order.type
        dict['status']=order.get_status()
        list.append(dict)
    args['orderList']=list
    args['result']='success'
    json=simplejson.dumps(args)
    return HttpResponse(json)
        
        
        
        
    
       
#############

    
@csrf_exempt
def pay_test(request):
    if request.method == 'GET' and request.GET.get('hub.mode') == 'subscribe':
#         mode=request.GET.get('hub.mode')
        challenge=request.GET.get('hub.challenge')
        verify_token=request.GET.get('hub.verify_token')
        return HttpResponse(challenge, content_type='text/plain')
    elif request.method == 'POST':
         post_body = simplejson.loads(request.body)
         object_type = post_body.get('object')
         entries = post_body.get('entry', [])
         logging.error("pay_test")
         logging.error(simplejson.dumps(object_type))
         logging.error(simplejson.dumps(entries))
         return HttpResponse()



def view_that_asks_for_money(request):
    from apps.pay_app.PayPal import asks_for_money
    args=asks_for_money(request)
    from apps.pay_app.models import Order
    orderList=Order.objects.filter(user_id=request.user.id).order_by('-createTime')
    args['orderList']=orderList
    from apps.pay_app.models import Charge
    charge=Charge.objects.get(user_id=request.user.id)
    args['charge']=charge
    return render(request,"payment.html", args)

@csrf_exempt
def paypal_notify(request):
    logging.error('payal通知')
    return HttpResponse('payal通知')

@csrf_exempt
def paypal_success(request):
    logging.error('paypal_success')
    return HttpResponse('paypal_success')

@csrf_exempt
def paypal_cancel(request):
    logging.error('paypal_cancel')
    return HttpResponse('paypal_cancel')



@csrf_exempt
def pay_test2(request):
    from django.contrib.auth.hashers import make_password
    make_password('2323223')
    return HttpResponse('222')
    