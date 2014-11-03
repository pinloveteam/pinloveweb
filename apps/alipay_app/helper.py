# -*- coding:utf-8 -*-

import socket
import struct
import urllib
from apps.alipay_app.alipay_setting import config
from apps.alipay_app.sign import sign
import logging
logger=logging.getLogger(__name__)

def address_in_network(ip, net):
    """
Is an address in a network
ip: 192.168.2.2
net:("192.168.2.0/24",)
"""
    ipaddr = struct.unpack('L',socket.inet_aton(ip))[0]
    for cur_net in net:
        netaddr,bits = cur_net.split('/')
        netmask = struct.unpack('L',socket.inet_aton(netaddr))[0] & ((2L<<int(bits)-1) - 1)
        if ipaddr & netmask == netmask:
            return True
    return False


def duplicate_out_trade_no(trade_obj):
    query = trade_obj._default_manager.filter(out_trade_no=trade_obj.out_trade_no)
    query = query.filter(trade_status=trade_obj.trade_status)
    return query.count() > 0

def get_form_data(form):
    """
if form is bound, return bound data
if form is initial, return initial data
"""
    data = {}
    if form.is_bound:
        data = form.data
    else: # unbound data
        for name, field in form.fields.items():
            if form.initial.has_key(name):
                data[name] = form.initial[name]
            elif field.initial:
                data[name] = field.initial
    return data

'''
     * 生成签名结果
     * @param kwargs 要签名的字典
     * @return 签名结果字符串
'''
def buildRequestMysign(kwargs):
    data=[]
    for k,v in kwargs.items():
        if k in ['sign','sign_type']:
            continue
        data.append('%s=%s'%(k,v))
    data.sort()
    text=u'&'.join(data)
    return unicode(sign(text,config.ALIPAY_KEY,config.ALIPAY_SIGN_TYPE))
    
def paraFilter(kwargs):
    result={}
    if kwargs==None or len(kwargs)==0:
        return result
    for key in kwargs.keys():
        if key in ['sign','sign_type'] and kwargs[key] in[None,'']:
            continue
        result[key]=kwargs[key]
    return result

def buildRequestPara(kwargs):
    params=paraFilter(kwargs)
    sign=buildRequestMysign(params)
    params["sign"]= sign
    params["sign_type"]=config.ALIPAY_SIGN_TYPE;
    
def urldecode(query):
    data = {}
    query_list = query.split('&')
    for kv in query_list:
        if kv.find('='):
            k,v = map(urllib.unquote_plus, kv.split('='))
            data[k] = v
    return data