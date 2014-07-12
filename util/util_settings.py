# -*- coding: utf-8 -*-
'''
Created on Sep 1, 2013

@author: jin
'''
from pinloveweb import settings
'''分页'''
from apps.recommend_app import recommend_settings
PAGE_NUM=getattr(recommend_settings, 'PAGE_NUM', 8)
BEVOR_RANGE_NUM=getattr(recommend_settings, 'BEVOR_RANGE_NUM', 4)
AFTER_RANGE_NUM=getattr(recommend_settings, 'AFTER_RANGE_NUM,', 4)


'''相册图片上传路径'''
IMAGE_UPLOAD_PATH_M='%s%s'%(settings.MEDIA_ROOT,'/images/')
'''相册图片上传路径相对路径'''
RELATRVE_IMAGE_UPLOAD_PATH_M='images/'

'''发布消息图片上传路径'''
PUBLIC_IMAGE_UPLOAD_PATH='%s%s'%(settings.MEDIA_ROOT,'/publish_img/')
'''相册图片上传路径相对路径'''
RELATRVE_PUBLIC_IMAGE_UPLOAD_PATH='publish_img/'


'''
邮件设置
'''
domain_name=u'http://www.pinpinlove.com/user/reset_password/'

'''
性格标签
'''
INIT_TAGS=(u'内向',u'急性子',u'节省',u'责任心强',u'幽默',u'乐观主义',u'细心',u'稳重',u'神经大条',u'独立',u'外向',u'慢性子',u'花钱',u'责任心一般',u'一般',u'悲观主义',u'不拘小节',u'冲动','多愁善感',u'依赖')

'''
cache
'''
PINTU=['GIRLS','BOYS','USER_GAME_COUNT','USER_GAME_COUNT_FOREVE','INVITE_COUNT','CONFIRM_INVITE']
EXPRESSION_REGEX=u'{:pinlove_[0-9]{1,2}:}'

