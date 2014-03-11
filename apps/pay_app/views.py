# -*- coding: utf-8 -*-
'''
Created on Sep 8, 2013

@author: jin
'''
from django.shortcuts import render
from apps.pay_app.models import FacebookPayDetail
from apps.third_party_login_app.models import FacebookUser
from django.utils import simplejson
from django.http.response import HttpResponse
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
    

def pay_test(request):
    mode=request.GET.get('hub.mode')
    challenge=request.GET.get('hub.challenge')
    verify_token=request.GET.get('hub.verify_token')
    return HttpResponse(challenge)
    
    