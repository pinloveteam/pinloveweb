#!/usr/bin/env python
# coding=utf-8
import logging
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
    for (k, v) in params.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
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
    if hasattr(v_json, 'error'):
        raise WeiXinError(v_json.error, v_json.error_description)

    if int(v_json['ret']) > 0:
        raise WeiXinError(v_json['ret'], v_json['msg'])

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
                 domain='api.weixin.qq.com', version='oauth2.0', display='default'):
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
        self.base_url = 'https://%s/' % domain


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
                  'scope': self.scope}
        params.update(kwargs)
        return '%s%s?%s' % ('https://open.weixin.qq.com/', 'connect/qrconnect', _encode_params(params))

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
        url = '%s%s/%s?%s' % (self.base_url,'sns/oauth2/access_token', _encode_params(params))
        resp = urllib2.urlopen(url)
        result = urlparse.parse_qs(resp.read(), True)
        access_token = str(result['access_token'][0])
        expires_in = float(int(result['expires_in'][0]) + int(time.time()))
        openid=str(result['openid'][0])
        refresh_token=result['openid'][0]
        
        self.set_access_token(access_token,expires_in)
        self.set_openid(openid)
        self.set_refresh_token(refresh_token)

        return {'access_token':access_token, 'expires_in': expires_in,'openid':openid,\
                'refresh_token':refresh_token}


    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def request_get_info(self, api='/sns/userinfo', method=_HTTP_GET, params={}):
        """
            普通api请求,需要传入api的调用名,如'/sns/userinfo'
        """

        #以下为默认的必传的公共参数
        params.update({'access_token': self.access_token,
                       'openid': self.openid})
        if self.is_expires():
            raise WeiXinError('21327', 'expired_token')
        return _http_request('%s%s' % (self.base_url, api), method, params, self.access_token)


