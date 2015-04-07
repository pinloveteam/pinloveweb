# -*- coding: utf-8 -*-
'''
Created on 2014年10月26日

@author: jin
'''
from django.utils import simplejson
from django.http.response import HttpResponse
import logging
logger=logging.getLogger(__name__)
def pay_tests(request):
    return confirm_callback_alipay(request)
'''
支付宝支付回调测试
'''   
from apps.pay_app.models import Order
def confirm_callback_alipay(request):
    args={}
    try:
        logging.error('%s%s'%('==============',request.META['REMOTE_ADDR']))
        from apps.alipay_app.signals import alipay_dpn_successful
        alipay_dpn_successful.send(sender=Order())
        args={'result':'success'}
    except Exception as e:
        args={'result':'error','error_message':e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)
    
'''
确认支付宝支付成功
'''
def confirm_alipay(request):
    try:
       from apps.alipay_app.models import AliPayDPN
       aliPayDPN=AliPayDPN(notify_type = 'trade_status_sync',out_trade_no='DD5ac0a9a5d-5fde-419',trade_status='TRADE_SUCCESS',total_fee=0.1)
       aliPayDPN.send_signals()
       args={'result':'success'}
    except Exception as e:
        args={'result':'error','error_message':e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)
    