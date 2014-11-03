#-*- coding: utf-8 -*-
# Create your views here.
'''
即时付款
'''
from apps.alipay_app.forms import AliPayDPNForm
import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.alipay_app.models import AliPayDPN
from django.http.response import HttpResponse
from django.utils import simplejson
logger=logging.getLogger(__name__)
@require_POST
@csrf_exempt
def dpn(request, item_check_callable=None):
   try:
    flag=None
    obj=None
    post_data=request.REQUEST.copy()
#     logger.error(simplejson.dumps(post_data))
    data={}
    for i,v in post_data.items():
        data[i]=v
    form=AliPayDPNForm(data)
    if form.is_valid():
        try:
            obj=form.save(commit=False)
        except Exception ,e:
            flag='Exception while processing: %s'% e
    else:
        flag='Invalid: %s'% form.errors
    if obj==None:
        obj = AliPayDPN()
        #Set query params and sender's IP address
    obj.initialize(request)
        
    if flag is not None:
        #We save errors in the flag field
        obj.set_flag(flag)
    else:
        logger.error('ip=====',obj.ipaddress)
        obj.verify(item_check_callable)
    obj.save()

    return HttpResponse('success')
   except Exception as e:
        logger.exception('即时付款出错!')
        args={'error_message':'即时付款出错!'}
        return render(request,'error.html',args)
    
def paid(request,template_name):
    args={}
    data=request.GET.copy()
    if data['trade_status']=='TRADE_SUCCESS':
        args={'title':'支付成功','content':'支付成功!','url':'/payment/menber/'}
    else:
        args={'title':'支付失败','content':'%s%s'%('支付失败!失败原因:',data['trade_status']),'url':'/payment/menber/'}
    return render(request,template_name,args)
        