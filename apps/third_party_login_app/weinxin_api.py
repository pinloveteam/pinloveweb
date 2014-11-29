#!/usr/bin/env python
# coding=utf-8
import logging
from django.utils import simplejson
__author__ = 'jin'
__version__ = '0.1.0'

import json
import time
import urllib, urllib2, urlparse
log=logging.getLogger(__name__)

def _obj_hook(pairs):
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class JsonObject(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def _encode_params(params):
    """
        将dict转换为url请求的参数形式:a=b&c=d
    """
    args = []
    keys=params.keys()
    keys.sort()
    for key in keys:
        qv = params[key].encode('utf-8') if isinstance(params[key], unicode) else str(params[key])
        args.append('%s=%s' % (key, urllib.quote(qv)))
    return '&'.join(args)

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_request(url, method, params, authorization):
    """
    执行http请求,目前两种格式,GET,POST
    """
    boundary = None
    args = _encode_params(params)

    http_url = '%s?%s' % (url, args) if method == _HTTP_GET else url
    http_params = None if method == _HTTP_GET else args

    req = urllib2.Request(http_url, http_params)

    if method == _HTTP_POST:
        req.add_header('POST %s HTTP/1.1')
    resp = urllib2.urlopen(req)
    body = str(resp.read())
    #body = body[9:-3]
    print body
    v_json = json.loads(body, object_hook=_obj_hook)
    if hasattr(v_json, 'errcode'):
        raise WeiXinError(v_json.error, v_json.error_description)

    return v_json

class WeiXinError(StandardError):
    def __init__(self, error, error_description):
        self.error =error
        self.error_description = error_description
        StandardError.__init__(self, error)

    def __str__(self):
        return 'WeiXinError: %s: %s' % (self.error, self.error_description)


class WeiXinClient(object):

    def __init__(self, client_id, client_secret, redirect_uri=None, response_type='code', scope='snsapi_login',state=None,
                 domain='api.weixin.qq.com', version='oauth2.0', display='default',type=2):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.domain = domain
        self.version = version
        self.response_type = response_type
        self.scope = scope
        self.display = display
        self.access_token = None
        self.openid = None
        self.refresh_token=None
        self.expires = 0.0
        self.state=state
        self.base_url = 'https://%s/' % domain
        #判断微信类型：开发者账号登录:1,公共账号：2
        self.type=type


    def set_access_token(self, access_token, expires_in):
        """
            设置access_token
        """
        self.access_token = access_token
        self.expires = expires_in


    def set_openid(self, openid):
        self.openid = openid
        
    def set_refresh_token(self,refresh_token):
        self.refresh_token=refresh_token

    def get_auth_url(self, redirect_uri=None,**kwargs):
        """
            获取登录的url,需要跳转至该url进行QQ登录
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        params = {'appid':self.client_id,
                  'response_type': self.response_type,
                  'redirect_uri': redirect,
                  'scope': self.scope,
                  'state':self.state}
        params.update(kwargs)
        return '%s%s?%s%s' % ('https://open.weixin.qq.com/', 'connect/qrconnect', urllib.urlencode(params),'#wechat_redirect' )
    
    '''
    公众号授权
    '''
    def public_authorization_url(self, redirect_uri=None,state=None):
        """
            获取登录的url,
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        state = state if state else self.state
        params = {'appid':self.client_id,
                  'response_type': self.response_type,
                  'redirect_uri': redirect,
                  'scope': self.scope,
                  'state':state}
        return '%s%s?%s%s' % ('https://open.weixin.qq.com/', 'connect/oauth2/authorize', _encode_params(params),'#wechat_redirect')

    def request_access_token(self, code, redirect_uri=None,**kwargs):
        """
            获得access_token,
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri

        #参数
        params = {'grant_type': 'authorization_code',
                  'appid': self.client_id,
                  'secret': self.client_secret,
                  'code': code,
                  'redirect_uri': redirect}
        params.update(kwargs)
        url = '%s%s?%s' % (self.base_url,'sns/oauth2/access_token', _encode_params(params))
#         log.error("url--------"+url)
        resp = urllib2.urlopen(url)
        result=simplejson.loads(resp.read())
        if u'errcode' in result.keys():
            raise WeiXinError(result['errcode'],result['errmsg'])
        else:
            access_token = str(result['access_token'])
            expires_in = float(int(result['expires_in']) + int(time.time()))
            openid=str(result['openid'])
            refresh_token=result['openid']
        
            self.set_access_token(access_token,expires_in)
            self.set_openid(openid)
            self.set_refresh_token(refresh_token)
            return {'access_token':access_token, 'expires_in': expires_in,'openid':openid,\
                'refresh_token':refresh_token}


    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def request_get_info(self, api='sns/userinfo', method=_HTTP_GET, params={}):
        """
            普通api请求,需要传入api的调用名,如'/sns/userinfo'
        """

        #以下为默认的必传的公共参数
        params.update({'access_token': self.access_token,
                       'openid': self.openid,
                       })
        if self.type==2:
           params['lang']=u'zh_CN'
#         if self.is_expires():
#             raise WeiXinError('21327', 'expired_token')
        return _http_request('%s%s' % (self.base_url, api), method, params, self.access_token)


if __name__ =='__main__':
    WeiXinAppID='wxdbf6f94c9d5f7cd1'
    WeiXinAppSecret='142757a23a30830e8f602fe82e5e4874'
    code=u''
    WEIXIN_CALLBACK_URL='http://pinlove.com/third_party_login/weixin_login/'
    access_token=u'OezXcEiiBSKSxW0eoylIeC-fBRcogV4Mueu3bqSaqJqYj0gO3aVk_R2PVN-qMam9tX0NjMcG8Hu_cR3x_PJxEfihm8by-OGqKo4zuVul00h_R7AR_zaitU2ft_8yM4y9B5_NRMNoF8XmSPmeoNZ1qQ'
    openid=u'oXDIAs63MJP-OqNOtfCEthkTOGo4'
    refresh_token=u'oXDIAs63MJP-OqNOtfCEthkTOGo4'
    expires_in=1416380655.0
    client = WeiXinClient(client_id=WeiXinAppID,client_secret=WeiXinAppSecret,redirect_uri=WEIXIN_CALLBACK_URL)
    if len(code)==0:
        client.set_access_token(access_token,expires_in)
        client.set_openid(openid)
        client.set_refresh_token(refresh_token)
        client.request_get_info()
    else:
        access=client.request_access_token(code)
        client.request_get_info()