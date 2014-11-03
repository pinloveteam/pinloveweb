#-*- coding: utf-8 -*-
from django.db import models
import urllib2
from apps.alipay_app.helper import address_in_network, duplicate_out_trade_no
from apps.alipay_app.alipay_setting import config, ALIPAY_NOTIFY_IP
from apps.alipay_app.signals import alipay_dpn_flagged, alipay_dpn_successful
from util.connection_db import connection_to_db
class AliPayBaseModel(models.Model):
    """
AliPay base model
"""
        # base parameter
    notify_time = models.DateTimeField(blank=True, null=True)
    notify_type = models.CharField(blank=True, null=True, max_length=32)
    #支付宝通知校验ID，商户可以用这个流水号询问支付宝该条通知的合法性。
    notify_id = models.CharField(blank=True, null=True, max_length=128,verbose_name=u'通知校验ID')
    sign_type = models.CharField(blank=True, null=True, max_length=3)
    sign = models.CharField(blank=True, null=True, max_length=64)
        # business parameter
        # partner trade no
    out_trade_no = models.CharField(blank=True, null=True, max_length=64,verbose_name=u'商户订单号')
    subject = models.CharField(blank=True, null=True, max_length=256)
    payment_type = models.CharField(blank=True, null=True, max_length=4)
        # alipay trade no
    trade_no = models.CharField(blank=True, null=True, max_length=64,verbose_name=u'支付宝交易号')
    trade_status = models.CharField(blank=True, null=True, max_length=32,verbose_name=u'交易状态')
    gmt_create = models.DateTimeField(blank=True, null=True)
    gmt_payment = models.DateTimeField(blank=True, null=True)
    refund_status = models.CharField(blank=True, null=True, max_length=32)
    gmt_refund = models.DateTimeField(blank=True, null=True)
    seller_email = models.CharField(blank=True, null=True, max_length=100)
    buyer_email = models.CharField(blank=True, null=True, max_length=100)
    seller_id = models.CharField(blank=True, null=True, max_length=30)
    buyer_id = models.CharField(blank=True, null=True, max_length=30)
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total_fee = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    body = models.CharField(blank=True, null=True, max_length=400)
    is_total_fee_adjust = models.CharField(blank=True, null=True, max_length=1) # Y/N
    use_coupon = models.CharField(blank=True, null=True, max_length=1) # Y/N
    
    # Non-AliPay Variables
    ipaddress = models.IPAddressField(blank=True)
    flag = models.BooleanField(default=False, blank=True,verbose_name=u'是否支付成功')
    flag_code = models.CharField(max_length=16, blank=True)
    flag_info = models.TextField(blank=True,verbose_name=u'错误信息')
    query = models.TextField(blank=True) # What we sent to PayPal.
    response = models.TextField(blank=True) # What we got back.
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.notify_id
    
    def is_transaction(self):
        if self.out_trade_no:
            return True
        else:
            return False

    def set_flag(self, info, code=None):
        """Sets a flag on the transaction and also sets a reason."""
        self.flag = True
        self.flag_info += info
        if code is not None:
            self.flag_code = code
        
    def verify(self, item_check_callable=None):
        """
verify alipay notify
"""
        self.response = self._postback()
        self._verify_postback()
        if not self.flag:
            if self.is_transaction():
                if not address_in_network(self.ipaddress,ALIPAY_NOTIFY_IP):
                    self.set_flag("Invalid alipay notify IP. (%s)" % self.ipaddress)
                if duplicate_out_trade_no(self):
                    self.set_flag("Duplicate out trade no. (%s)" % self.out_trade_no)
                if self.seller_id != config.ALIPAY_SELLER_ID:
                    self.set_flag("Invalid seller id. (%s)" % self.seller_id)
                if callable(item_check_callable):
                    flag, reason = item_check_callable(self)
                    if flag:
                        self.set_flag(reason)
            else:
                # @@@ Run a different series of checks on recurring payments.
                pass
        
        self.save()
        self.send_signals()

    def send_signals(self):
        raise NotImplementError

    def initialize(self, request):
        """Store the data we'll need to make the postback from the request object."""
        self.query = getattr(request, request.method).urlencode()
        self.notify_id = getattr(request, request.method).get('notify_id')
        self.ipaddress = request.META.get('REMOTE_ADDR', '')

    def _postback(self):
        return urllib2.urlopen(config.ALIPAY_GATEWAY,'service=notify_verify&partner=%s&notify_id=%s'% (config.ALIPAY_PARTNER, self.notify_id)).read()

    def _verify_postback(self):
        if self.response != "true":
            self.set_flag("Invalid postback: %s" % self.response)
            
      
class AliPayDPNManager(models.Manager):
    '''
    统计金额
    @param startTime(option):起始时间
    @param endTime(option):  结束时间
    '''
    def statistic_price(self,**kwargs):
        sqlTime=''
        if kwargs.get("startTime",'')!='':
            sqlTime=' where gmt_payment >= %s and gmt_payment <= '%(kwargs.get("startTime",''),kwargs.get("endTime",''))
        sql="""
           select sum(u.total_fee) from alipay_dpn u where u.trade_status='TRADE_SUCCESS'
           """+sqlTime
        return connection_to_db(sql,param=[],type=True)
'''
即时支付
'''           
class AliPayDPN(AliPayBaseModel):
    """
AliPay DPN
"""
    gmt_close = models.DateTimeField(blank=True, null=True)
    extra_common_param = models.CharField(blank=True, null=True, max_length=256)
    out_channel_type = models.CharField(blank=True, null=True, max_length=256)
    out_channel_amount = models.CharField(blank=True, null=True, max_length=256)
    out_channel_inst = models.CharField(blank=True, null=True, max_length=256)

    class Meta:
        db_table = 'alipay_dpn'
        verbose_name = 'AliPay DPN'
        
    def send_signals(self):
        if self.notify_type != 'trade_status_sync':
            return
        if self.is_transaction():
            if self.flag:
                alipay_dpn_flagged.send(sender=self)
            else:
                alipay_dpn_successful.send(sender=self)
