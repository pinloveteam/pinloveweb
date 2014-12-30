# -*-coding: utf-8 -*-
'''
Created on 2014年7月7日

@author: jin
'''
from apps.friend_dynamic_app.models import FriendDynamicComment,\
    FriendDynamicArgee, Picture
'''
根据用户id获取未读消息数量
'''
def get_no_read_comment_count(userId):
    return FriendDynamicComment.objects.get_no_read_comment_count(userId)

'''
根据id列表将评论标记成已读
@param ids:id列表 
'''
def clean_dynamic_comment_by_ids(ids):
    FriendDynamicComment.objects.filter(id__in=ids).update(isRead=True)
  
'''
根据id列表将点赞标记成已读
@param ids:id列表 
'''  
def clean_dynamic_argee_by_ids(ids):
    FriendDynamicArgee.objects.filter(id__in=ids).update(isRead=True)
  
'''
获取点赞的未读数量
'''  
def get_no_read_agree_count(userId):
    return FriendDynamicArgee.objects.get_no_read_agree_count(userId)


def get_pic(userId,first=0,end=100):
    pictureBeanList=[]
    pictureList=Picture.objects.filter(user_id=userId).order_by('-createTime')[first:end]
    for picture in pictureList:
        from apps.friend_dynamic_app.dynamic_settings import IMAGE_SAVE_FORMAT,thumbnails
        smailPic='%s%s%s%s%s'%(picture.picPath,'-',thumbnails[0],'.',IMAGE_SAVE_FORMAT)
        pic='%s%s%s'%(picture.picPath,'.',IMAGE_SAVE_FORMAT)
        pictureBeanList.append({'description':picture.description,'pic':pic,'smailPic':smailPic,'createTime':picture.createTime.strftime("%Y-%m-%d-%H")})
    return pictureBeanList
     
            