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
    paymentId=request.REQUEST.get('payment_id',False)
    amount=float(request.REQUEST.get('amount',False))
    currency=request.REQUEST.get('currency',False)
    quantity=int(request.REQUEST.get('quantity',False))
    signed_request=request.REQUEST.get('signed_request',False)
    status=request.REQUEST.get('completed',False)
    FacebookPayDetail(id=paymentId,amount=amount,currency=currency,quantity=quantity,status=status,signed_request=signed_request)
    if status=='compelet':
        uid=request.user.uid
        price=FacebookUser.objects.get(uid=uid).price
        price=price+quantity
        FacebookUser.objects.filter(uid=uid).update(price=price)

    
    
    