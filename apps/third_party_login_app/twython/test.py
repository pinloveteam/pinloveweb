# -*- coding: utf-8 -*-
'''
Created on Dec 17, 2013

@author: jin
'''
from apps.third_party_login_app.setting import TwitterConsumerKey,\
    TwitterConsumerSecret
from apps.third_party_login_app.TwitterAPI import TwitterAPI
from apps.third_party_login_app.twython.api import Twython
# access_token_key='2249878794-QGk7iGnMgFQZAttHYV1HJjbkjTJTkFtOR6PqVsn'
# access_token_secret='9AsQvWkKEYai7u65TMH2Fcnqcvp6tdV04XPGUNFN5C3Te'
# api = TwitterAPI(TwitterConsumerKey, TwitterConsumerSecret, access_token_key, access_token_secret)
twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret)
auth = twitter.get_authentication_tokens(callback_url='')
# OAUTH_TOKEN ='vQO8ljARqbGPqx1gv3LDlpuamB1tBd2jnQn3cCsslwo'
# OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
access=twitter.get_authorized_tokens('kQjnN27qCiuwezOXfgY2WnoMcRa3mYLyAqwEuAIWhs')
# twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
# auth = twitter.get_authentication_tokens(callback_url='http://snailjin.eicp.net/third_party_login/twitter_login_url/')
# print auth['oauth_token']
# i=twitter.show_user()
# i=twitter.verify_credentials()
print access