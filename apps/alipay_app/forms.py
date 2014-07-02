#-*- coding: utf-8 -*-
'''
Created on 2014年6月28日

@author: jin
'''
from django import forms
from apps.alipay_app.alipay_setting import config, SERVICE, PAYMENT_TYPE,\
    ALIPAY_DATE_FORMAT
from paypal.standard.widgets import ValueHiddenInput
from django.utils.safestring import mark_safe
from apps.alipay_app.helper import get_form_data, buildRequestMysign
from apps.alipay_app.models import AliPayDPN
class AliPayPaymentBaseForm(forms.Form):
    """
request interface. POST method, HTTPS
"""
        # base parameters
    service = forms.CharField(widget=ValueHiddenInput(), initial=SERVICE[0])
    partner = forms.CharField(widget=ValueHiddenInput(), max_length=16, initial=config.ALIPAY_PARTNER)
    # 商户网站使用的编码格式，如utf-8、gbk、gb2312等
    _input_charset = forms.CharField(widget=ValueHiddenInput(), initial=config.ALIPAY_INPUT_CHARSET)
    # DSA、RSA、MD5三个值可选，必须大写
    sign_type = forms.CharField(widget=ValueHiddenInput(), initial=config.ALIPAY_SIGN_TYPE)
    sign = forms.CharField(widget=ValueHiddenInput())
    notify_url = forms.CharField(widget=ValueHiddenInput())
    return_url = forms.CharField(widget=ValueHiddenInput())
    # 需开通
    error_notify_url = forms.CharField(widget=ValueHiddenInput())
    # business parameters
    out_trade_no = forms.CharField(widget=ValueHiddenInput(), max_length=64)
    subject = forms.CharField(widget=ValueHiddenInput(), max_length=256)
    payment_type = forms.CharField(widget=ValueHiddenInput(), initial=PAYMENT_TYPE[0])
        # 买家 卖家 信息
    seller_id = forms.CharField(widget=ValueHiddenInput(), max_length=32, initial=config.ALIPAY_SELLER_ID)
    buyer_id = forms.CharField(widget=ValueHiddenInput(), max_length=32)
    seller_account_name = forms.CharField(widget=ValueHiddenInput(), max_length=100)
    buyer_account_name = forms.CharField(widget=ValueHiddenInput(), max_length=100)
    seller_email = forms.CharField(widget=ValueHiddenInput(), max_length=100)
    buyer_email = forms.CharField(widget=ValueHiddenInput(), max_length=100)
        # 买家逾期不付款，自动关闭交易
    it_b_pay = forms.CharField(widget=ValueHiddenInput())
        # 价格 unit: RMB
    price = forms.FloatField(widget=ValueHiddenInput(), min_value=0.01, max_value=1000000.00)
    quantity = forms.IntegerField(widget=ValueHiddenInput())
        # 担保交易不支持 total_fee
    total_fee = forms.FloatField(widget=ValueHiddenInput(), min_value=0.01, max_value=1000000.00)
    body = forms.CharField(widget=ValueHiddenInput(), max_length=1000)
    show_url = forms.CharField(widget=ValueHiddenInput(), max_length=400)
    paymethod = forms.CharField(widget=ValueHiddenInput())
    discount = forms.FloatField(widget=ValueHiddenInput())
        # CTU 支付宝风险稽查系统，需开通
    need_ctu_check = forms.CharField(widget=ValueHiddenInput()) # Y/N
    royalty_type = forms.CharField(widget=ValueHiddenInput(), max_length=2) # 10
    royalty_parameters = forms.CharField(widget=ValueHiddenInput())
        # 需开通
    anti_phishing_key = forms.CharField(widget=ValueHiddenInput())
        # 需开通
    exter_invoke_ip = forms.CharField(widget=ValueHiddenInput(), max_length=15)
    extra_common_param = forms.CharField(widget=ValueHiddenInput(), max_length=100)
    extend_param = forms.CharField(widget=ValueHiddenInput())
    default_login = forms.CharField(widget=ValueHiddenInput()) # Y/N
    product_type = forms.CharField(widget=ValueHiddenInput(), max_length=50)
        # 需开通快捷登录
    token = forms.CharField(widget=ValueHiddenInput(), max_length=40)
    
    def get_action(self):
        return '%s?_input_charset=%s'% (config.ALIPAY_GATEWAY, self['_input_charset'].value())
 
class AliPayBaseForm(forms.ModelForm):
    """
Some models field
"""
    notify_time = forms.DateTimeField(required=False,input_formats=ALIPAY_DATE_FORMAT)
    gmt_create = forms.DateTimeField(required=False, input_formats=ALIPAY_DATE_FORMAT)
    gmt_payment = forms.DateTimeField(required=False, input_formats=ALIPAY_DATE_FORMAT)
    gmt_close = forms.DateTimeField(required=False, input_formats=ALIPAY_DATE_FORMAT)
    gmt_refund = forms.DateTimeField(required=False, input_formats=ALIPAY_DATE_FORMAT)
    gmt_logistics_modify = forms.DateTimeField(required=False, input_formats=ALIPAY_DATE_FORMAT)

    def clean_sign(self):
        data = get_form_data(self)
        sign = buildRequestMysign(data)
        if sign != data.get('sign'):
            self._errors['sign'] = self.error_class(['sign error!'])
        return sign 
'''
即时付款
'''  
class AliPayDirectPayForm(AliPayPaymentBaseForm):
    def __init__(self,*args,**kwargs):
        AliPayPaymentBaseForm.__init__(self,*args,**kwargs)
    service = forms.CharField(widget=ValueHiddenInput(), initial=SERVICE[0])
    '''
    生成html的form表单
    '''
    def render(self):
        return mark_safe(u"""<form action="%s" method="post">
    %s
    <input type="image" src="%s" border="0" name="submit" alt="Buy it Now" />
</form>""" % (self.get_action(), self.as_p(), ''))
        
        
class AliPayDPNForm(AliPayBaseForm):
    """
AliPay Direct Payment Notify Form
"""
    class Meta:
        model = AliPayDPN