# -*-coding: utf-8 -*-
'''
Created on Nov 5, 2013

@author: jin
'''
from django.shortcuts import render
from apps.friend_dynamic_app.models import FriendDynamic, Picture,\
    FriendDynamicComment, FriendDynamicArgee
from pinloveweb import settings
from PIL import ImageFile 
import time
from apps.user_app.models import UserProfile, Follow
from django.utils import simplejson
from django.http import HttpResponse
import logging
from django.http.response import HttpResponseRedirect
from util.page import page
logger=logging.getLogger(__name__)
'''
卡片界面动态
发动态
'''
def dynamic(request):
    arg={}
    dynamicId=request.REQUEST.get('dynamicId',None)
    #发布动态
    if request.method=="POST":
        flag=True
        content=request.POST.get('content').strip()
        if content.rstrip()=='':
            arg['error']={'error':u'发布内容不能为空！'}
            flag=False
        friendDynamic=FriendDynamic()
        friendDynamic.publishUser=request.user
        friendDynamic.content=content
        if 'images_path' in request.session.keys():
            friendDynamic.data=request.session['images_path']
            friendDynamic.type=2
        else:
            friendDynamic.type=1
        friendDynamic.save()
        if 'images_path' in request.session.keys():
#             pictureList=[]
            photoList=simplejson.loads(request.session['images_path'])
            for photo in photoList:
                picture=Picture()
                picture.user=request.user
                picture.friendDynamic=friendDynamic
                picture.description=content
                from util import util_settings
                picture.picPath='%s%s' % (util_settings.RELATRVE_IMAGE_UPLOAD_PATH_M,photo)
                picture.save()
                del request.session['images_path']
#                 pictureList.append(picture.picPath)
        return HttpResponseRedirect('/dynamic/')
    userProfile=UserProfile.objects.get(user_id=request.user.id)
    from pinloveweb.method import init_person_info_for_card_page
    arg.update(init_person_info_for_card_page(userProfile))
    arg=init_dynamic(request,request.user.id,arg,0,dynamicId=dynamicId)
    if request.GET.get('type')=='ajax':
        from apps.pojo.dynamic import MyEncoder
        json=simplejson.dumps( {'friendDynamicList':arg['friendDynamicList'],'next_page_number':arg['next_page_number']},cls=MyEncoder)
        return HttpResponse(json, mimetype='application/json')
    if  'images_path' in request.session:
        del request.session['images_path']
    return render(request, 'dynamic.html',arg )

'''
用户个人动态中心
'''
def person_dynamic(request):
    arg={}
    try:
        userId=int(request.REQUEST.get('userId'))
        arg['userId']=userId
        userProfile=UserProfile.objects.get(user_id=request.user.id)
        from pinloveweb.method import init_person_info_for_card_page
        arg.update(init_person_info_for_card_page(userProfile))
        arg=init_dynamic(request,userId,arg,1)
        if request.GET.get('type')=='ajax':
            from apps.pojo.dynamic import MyEncoder
            json=simplejson.dumps( {'friendDynamicList':arg['friendDynamicList'],'next_page_number':arg['next_page_number']},cls=MyEncoder)
            return HttpResponse(json, mimetype='application/json')
        return render(request, 'person_dynamic.html',arg )
    except:
        logger.expction('用户个人动态中心,出错!')
'''
初始化动态
attridute 
  type 
     0   好友动态
     1   自己的动态
@param dynamicId:d动态id获取单条动态 
'''
def init_dynamic(request,userId,arg,type=None,**kwargs):
    from apps.pojo.dynamic import friendDynamicList_to_Dynamic
    #获取单条消息列表
    if not kwargs.get('dynamicId') is None:
        friendDynamicList=FriendDynamic.objects.filter(id=kwargs.get('dynamicId'))
        arg['friendDynamicList']=friendDynamicList_to_Dynamic(friendDynamicList, userId)
        return arg
    elif type==0:
        friendDynamicList=FriendDynamic.objects.get_follow_list(userId)
    else:
        friendDynamicList=FriendDynamic.objects.filter(publishUser_id=userId).order_by('-publishTime')
    arg.update(page(request,friendDynamicList))
    friendDynamicList=friendDynamicList_to_Dynamic(arg['pages'].object_list, userId)
    #获取点赞列表
#     friendDynamicArgeeList=FriendDynamicArgee.objects.filter(user=user)
#     argeeList=[]
#     for friendDynamic in friendDynamicList:
#         commentNum=FriendDynamic.objects.get_coment_count(friendDynamic.publishUser.id,user.id,friendDynamic.id)
#         friendDynamic.commentNum=commentNum
#         if friendDynamic.type==2:
#             friendDynamic.data=simplejson.loads(friendDynamic.data)
#         is_agreee=False  
#         for friendDynamicArgee in friendDynamicArgeeList:
#             if friendDynamic.id==friendDynamicArgee.friendDynamic_id:
#                 is_agreee=True 
#         argeeList.append(is_agreee)  
    arg['friendDynamicList']=friendDynamicList
    if arg['pages'].has_next():
        arg['next_page_number']=arg['pages'].next_page_number()
    else:
        arg['next_page_number']=-1
#     arg['argeeList']=argeeList
    return  arg

'''
获取评论列表
如有未读消息显示未读，否则已读显示已读
'''
def comment_list(request):
    args={}
    try:
        if request.is_ajax():
            if FriendDynamicComment.objects.get_no_read_comment_count(request.user.id)>0:
                friendDynamicCommentList=FriendDynamicComment.objects.get_no_read_comment_list(request.user.id)
                data=page(request,friendDynamicCommentList)
                friendDynamicIds=[friendDynamic['id'] for friendDynamic in data['pages'].object_list]
                FriendDynamicComment.objects.filter(id__in=friendDynamicIds).update(isRead=True)
            else:
                 friendDynamicCommentList=FriendDynamicComment.objects.get_comment_list(request.user.id)
                 data=page(request,friendDynamicCommentList)
            from apps.pojo.message import messagedynamics_to_message_page
            messageList=messagedynamics_to_message_page(data['pages'].object_list)
            args['messageList']=messageList
            if data['pages'].has_next():
                #如果为未读
                if data['pages'].object_list[0]['isRead']:
                    args['next_page_number']=1
                else:
                    args['next_page_number']=data['pages'].next_page_number()
            else:
                data['next_page_number']=-1
            json=simplejson.dumps(args)
            return HttpResponse(json)    
    except Exception,e:
        logger.exception('获取评论列表,出错')

'''
获得赞的列表
'''
def agree_list(request):
    args={}
    try:
        if request.is_ajax():
            if FriendDynamicArgee.objects.get_no_read_agree_count(request.user.id)>0:
                friendDynamicArgeeList=FriendDynamicArgee.objects.get_no_read_agree_List(request.user.id)
                data=page(request,friendDynamicArgeeList)
                friendDynamicIds=[friendDynamic['id'] for friendDynamic in data['pages'].object_list]
                FriendDynamicArgee.objects.filter(id__in=friendDynamicIds).update(isRead=True)
            else:
                friendDynamicArgeeList=FriendDynamicArgee.objects.get_agree_List(request.user.id)
                data=page(request,friendDynamicArgeeList)
            from apps.pojo.message import messagedynamics_to_message_page
            messageList=messagedynamics_to_message_page(data['pages'].object_list)
            args['messageList']=messageList
            if data['pages'].has_next():
                #如果为未读
                if data['pages'].object_list[0]['isRead']:
                    args['next_page_number']=1
                else:
                    args['next_page_number']=data['pages'].next_page_number()
            else:
                data['next_page_number']=-1
            json=simplejson.dumps(args)
            return HttpResponse(json)    
    except Exception,e:
        logger.exception('获取赞的列表,出错')

'''
获取未读评论列表
'''
def no_read_comment_list(request,template_name):
    args={}
    try:
        user=request.user
        userProfile=UserProfile.objects.get(user=user)
        commentList=FriendDynamicComment.objects.get_no_read_comment_by_user_id(user.id)
        args=page(request,commentList)
        from apps.pojo.dynamic import FriendDynamicCommentList_to_CommentDynamicList
        args['pages'].object_list=FriendDynamicCommentList_to_CommentDynamicList(args['pages'].object_list)
        commentList.update(isRead=True)
        if args['pages'].has_next():
            args['next_page_number']=args['pages'].next_page_number()
        else:
            args['next_page_number']=-1
        #初始化个人信息模块
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        if request.is_ajax():
            from django.core.serializers.json import DjangoJSONEncoder
            json=simplejson.dumps( {'friendDynamicCommentList':args['pages'].object_list,'next_page_number':args['next_page_number']},cls=DjangoJSONEncoder)
            return HttpResponse(json, mimetype='application/json')
        return render(request,template_name,args)
    except Exception,e:
        logger.exception('获取未读评论列表,出错')
###############################################
##以上用用于1.0版
########################################
'''
 发布消息
'''
logger = logging.getLogger('django_request_logfile')
def send_dynamic(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=="POST":
            flag=True
            type=request.POST.get('type').strip()
            content=request.POST.get('content').strip()
            #判断失败条件
            if int(type)>=3:
                arg['error']={'error':u'发布失败！'}
                flag=False
            if content.rstrip()=='':
                arg['error']={'error':u'发布内容不能为空！'}
                flag=False
            friendDynamic=FriendDynamic()
            friendDynamic.publishUser=request.user
            friendDynamic.type=type
            friendDynamic.content=content
            if type=='2':
                friendDynamic.data=request.session['images_path']
            friendDynamic.save()
            if type=='2':
                photoList=simplejson.loads(request.session['images_path'])
                for photo in photoList:
                    picture=Picture()
                    picture.user=request.user
                    picture.friendDynamic=friendDynamic
                    picture.description=content
                    from util import util_settings
                    picture.picPath='%s%s' % (util_settings.RELATRVE_IMAGE_UPLOAD_PATH_M,photo)
                    picture.save()
                del request.session['images_path']
            arg=init_dynamic(request.user,arg)
            if flag:
                return render(request, 'send_dynamic.html', arg,)
            else:
                return render(request, 'send_dynamic.html', arg,)
        else:
            arg=init_dynamic(request.user,arg)
            return render(request, 'send_dynamic.html', arg,)      
    else:
        return render(request, 'login.html', arg,)   

'''
 删除消息
'''
def del_dynamic(request):
    arg={}
    if request.user.is_authenticated():
        id=int(request.GET.get('id'))
        type=int(request.GET.get('type'))
        if type==1:
            FriendDynamic.objects.get(id=id).delete()
            from pinloveweb.method import get_dymainc_late
            arg['dynamic']= get_dymainc_late(request.user.id)
            arg['type']='success'
        elif type==2:
#             Picture.objects.filter(friendDynamic_id=id).delete()
            FriendDynamic.objects.get(id=id).delete()
            arg['type']='success'
        else:
            arg['type']='error'  
    else:
        arg['type']='login'
    json=simplejson.dumps(arg)
    return HttpResponse(json)

def dynamic_list(request):
    arg={}
    if request.user.is_authenticated():
        friendDynamicList=FriendDynamic.objects.filter(publishUser=request.user)
    else:
        return render(request, 'login.html', arg,) 
'''
上传动态图片
'''  
def update_photo(request): 
  try:
    if request.method == 'POST':
      if request.FILES :
        arg={}
        # uppload image
        f = request.FILES["file"]
        type=request.POST.get('type',False)
        parser = ImageFile.Parser()  
        for chunk in f.chunks():
            parser.feed(chunk)  
        img = parser.close()
        from util import util_settings
        from util.util import random_str
        pictureName='%s%s%s%s' % (request.user.id,'_',time.strftime('%Y%m%d',time.localtime(time.time())),random_str(randomlength=10))
        if not  type:
         if 'images_path' in request.session.keys():
            list=simplejson.loads(request.session['images_path'])
            list.append(pictureName)
            request.session['images_path']=simplejson.dumps(list)
         else:
            request.session['images_path']=simplejson.dumps([pictureName,])
        name = '%s%s' % (util_settings.IMAGE_UPLOAD_PATH_M,pictureName)
        from apps.friend_dynamic_app.dynamic_settings import thumbnails,IMAGE_SAVE_FORMAT
        img.save('%s%s%s'%(name,'.',IMAGE_SAVE_FORMAT))
        img.thumbnail(thumbnails)
        img.save('%s%s%s%s%s'%(name,'-',thumbnails[0],'.',IMAGE_SAVE_FORMAT))
#         return HttpResponseRedirect('/dynamic/send/')
        return HttpResponse(pictureName)
  except :
        logger.exception('上传动态图片出错！')
        return HttpResponse('上传图片出错!')

'''
删除图片
attribute:图片名称
'''
def delete_photo(request):
        try:
            pictureName=request.GET.get('pictureName')
        except:
            logger.error('获取图片名称pictureName失败')
            logging.exception('Got exception on main handler')
        if 'images_path' in request.session.keys():
            list=simplejson.loads(request.session['images_path'])
            if pictureName in list:
                list.remove(pictureName)
        from util import util_settings
        name = '%s%s' % (util_settings.IMAGE_UPLOAD_PATH_M,pictureName)
        from apps.friend_dynamic_app.dynamic_settings import IMAGE_SAVE_FORMAT,thumbnails
        path='%s%s%s'%(name,'.',IMAGE_SAVE_FORMAT)
        thumbnailPath='%s%s%s%s%s'%(name,'-',thumbnails[0],'.',IMAGE_SAVE_FORMAT)
        import os
        os.remove(path)
        os.remove(thumbnailPath)
        return HttpResponse('删除成功!')
    
def update_video(request): 
    arg={}
    if request.user.is_authenticated():
        if request.method == 'POST':
            if request.FILES :
                f = request.FILES["file"]
    else:
        return HttpResponse("请先登录")
'''
添加删除点赞
'''
def agree(request):
    arg={}
    if request.user.is_authenticated():
        try:
            id=int(request.GET.get('id'))
        except:
            arg['type']='error' 
            json=simplejson.dumps(arg)
            return json
        argeeNum=FriendDynamic.objects.get(id=id).argeeNum
        if FriendDynamicArgee.objects.filter(friendDynamic_id=id,user=request.user).exists():
            FriendDynamicArgee.objects.get(friendDynamic_id=id).delete()
            argeeNum=argeeNum-1
            FriendDynamic.objects.filter(id=id).update(argeeNum=argeeNum)
            arg['type']='delSuccess'
        else:
            friendDynamicArgee=FriendDynamicArgee()
            friendDynamicArgee.friendDynamic_id=id
            friendDynamicArgee.user=request.user
            friendDynamicArgee.save()
            argeeNum=argeeNum+1
            FriendDynamic.objects.filter(id=id).update(argeeNum=argeeNum)
            arg['type']='addSuccess'  
    else:
        arg['type']='login'
    json=simplejson.dumps(arg)
    return HttpResponse(json)
    
'''
查看评论
'''
def show_comment(request):
    arg={}
    try:
        dynamicId=int(request.GET.get('id'))
        publishUserId=int(request.GET.get('publishUserId'))
    except:
        arg['type']='error' 
        json=simplejson.dumps(arg)
        return json
    if publishUserId==request.user.id:
         commentList=FriendDynamicComment.objects.select_related('reviewer','receiver').filter(friendDynamic_id=dynamicId).order_by('-commentTime')
    else:
        from django.db.models.query_utils import Q
        commentList=FriendDynamicComment.objects.select_related('reviewer','receiver').filter(Q(friendDynamic_id=dynamicId,reviewer_id__in=[request.user.id,publishUserId],receiver_id__in=[request.user.id,publishUserId])|Q(friendDynamic_id=dynamicId,receiver_id__isnull=True)).order_by('-commentTime')
    #标记为已读
    commentIds=[comment.id for comment in commentList if comment.receiver_id==request.user.id]
    FriendDynamicComment.objects.filter(id__in=commentIds).update(isRead=True)
    from apps.pojo.dynamic import FriendDynamicCommentList_to_DynamicCommentList
    dynamicCommentList=FriendDynamicCommentList_to_DynamicCommentList(commentList)
    from apps.pojo.dynamic import DynamicCommentEncoder
    json=simplejson.dumps(dynamicCommentList,cls=DynamicCommentEncoder)
    return HttpResponse(json)

'''
发布评论
'''
def comment(request):
        arg={}
        try:
            dynamicId=int(request.REQUEST.get('dynamicId'))
            receiverId=request.REQUEST.get('receiverId','')
            content=request.REQUEST.get('content')
        except:
            arg['type']='error' 
            json=simplejson.dumps(arg)
            return HttpResponse(json)
        comment=FriendDynamicComment()
        if len(receiverId)<=0:
            friendDynamic=FriendDynamic.objects.select_related('publishUser').get(id=dynamicId)
            if friendDynamic.publishUser.id!=request.user.id:
                comment.receiver_id=friendDynamic.publishUser.id
        elif int(receiverId)==request.user.id:
            arg={'type':'error','msg':'能自己对自己评论'}
            json=simplejson.dumps(arg)
            return HttpResponse(json)
        else:
            comment.receiver_id=receiverId
        if content.startswith(u'回复@'):
            comment.content=content[content.index(':')+1:]
        else:
            comment.content=content
        comment.friendDynamic_id=dynamicId
        comment.reviewer=request.user
        #如果对自己的动态回复，则向每个回复过你的人发送动态
        if comment.receiver_id==request.user.id:
            myComments=FriendDynamicComment.objects.filter(friendDynamic_id=dynamicId)
            reviewerIds=[]
            for commentI in myComments:
                if not (commentI.reviewer_id in reviewerIds or commentI.reviewer_id ==request.user.id):
                    reviewerIds.append(commentI.reviewer_id)
            for reviewerId in reviewerIds:
               comment.receiver_id=reviewerId
               comment.id=None
               comment.save()
        else:
            comment.save()
        commentNum=FriendDynamic.objects.get(id=dynamicId).commentNum
        FriendDynamic.objects.filter(id=dynamicId).update(commentNum=commentNum+1)
        from apps.pojo.dynamic import FriendDynamicCommentList_to_DynamicCommentList
        dynamicCommentList=FriendDynamicCommentList_to_DynamicCommentList([comment,])
        arg['type']='success'
        arg['dynamicCommentList']=dynamicCommentList
        from apps.pojo.dynamic import DynamicCommentEncoder
        json=simplejson.dumps(arg,cls=DynamicCommentEncoder)
        return HttpResponse(json)  

'''
删除评论
'''
def del_comment(request):
    arg={}
    commentId=int(request.GET.get('commentId'))
    if FriendDynamicComment.objects.filter(reviewer=request.user,id=commentId).exists():
        FriendDynamicComment.objects.filter(reviewer=request.user,id=commentId).delete()
#         commentNum=FriendDynamic.objects.get(id=friendDynamicComment.friendDynamic_id).commentNum
#         FriendDynamic.objects.filter(id=friendDynamicComment.friendDynamic_id).update(commentNum=commentNum-1)
    else:
        arg['type']='error'
        arg['msg']='数据错误'
    arg['type']='success'
    json=simplejson.dumps(arg)
    return HttpResponse(json)



#用于初始化card页面所需要的信息
def init_card(arg,userProfile):
    if userProfile.avatar_name_status!='3':
        arg['avatar_name']='user_img/image.png'
    else:
        arg['avatar_name']=userProfile.avatar_name
    arg['age']=userProfile.age
    arg['height']=userProfile.height
    arg['income']=userProfile.income
    arg['education']=userProfile.get_education_display()
    arg['jobIndustry']=userProfile.jobIndustry
    return arg
   
