#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.game_app.models import Yuanfenjigsaw, get_count
from apps.third_party_login_app.models import FacebookUser


@csrf_exempt
def jigsaw(request):
    match_result = Yuanfenjigsaw(request).get_match_result()
    json=simplejson.dumps(match_result)
    return HttpResponse(json, mimetype='application/javascript')

def jigsaw_mobi(request):
    callback = request.GET.get('callback')
    match_result = Yuanfenjigsaw(request).get_match_result()
    json=callback + '('+simplejson.dumps(match_result)+')'
    return HttpResponse(json)
def pintu(request):
    from apps.third_party_login_app.models import FacebookUser
    username=FacebookUser.objects.get(uid=request.facebook.uid).username
    count = get_count(username)
    return render(request, 'pintu.html',{'count':count})

'''
邀请好友确认，奖励
'''
def confirm_request_life(request,offset):
    args={}
    userUid=request.session['apprequest']
    if offset in userUid:
        from apps.game_app.models import get_game_count_forever,set_game_count_forever,get_invite_count,set_invite_count
        import logging
        logging.error('%s' % (request.facebook))
        invite_count=get_invite_count(offset)+1
        from django.core.cache import cache
        if (invite_count-cache.get('INVITE_TIME_A_LIFE'))>=0:
            set_invite_count(offset,invite_count-3)
            set_game_count_forever(offset,get_game_count_forever(offset)+1)
        else:
            set_invite_count(offset,invite_count)
        userUid.remove(offset)
        request.session['apprequest']=userUid
        args['result']='success'
        #添加确认邀请名单
        from apps.third_party_login_app.models import FacebookUser
        user=FacebookUser.objects.get(uid=request.session['uid'])
        from apps.game_app.models import has_invited,add_invite_confirm
        if not has_invited(offset,user.username):
            add_invite_confirm(offset,user.username)
        inviteConfirm= cache.get('CONFIRM_INVITE')
#         from apps.third_party_login_app.models import FacebookUser
#         username=FacebookUser.objects.get(uid=uid).username
#         args['count']=get_count(username)+get_game_count_forever(uid)
    else:
        args['result']='error'
    json=simplejson.dumps(args)
    return HttpResponse(json, mimetype='application/javascript')
'''
重置缓存数据
'''       
def reset_game_cache(request):
    from apps.game_app.models import reset_game
    reset_game()
    from django.core.cache import cache
    girls=cache.get('GIRLS')
    boys=cache.get('BOYS')
    return render(request,'debug_cache.html',{'girls':girls,'boys':boys})

def recommend_history(request):
    uid=request.session['uid']
    recommendHistoryList=simplejson.loads(FacebookUser.objects.get(uid=uid).recommendList)
    facebookUserList=FacebookUser.objects.filter(uid__in=recommendHistoryList)
    from util.util import model_to_dict
    facebookUserListDcit=model_to_dict(facebookUserList, fields=['uid','username','avatar','location']) 
    json=simplejson.dumps(facebookUserListDcit)
#     from django.core import serializers
#     json=serializers.serialize('json', FacebookUser.objects.filter(uid__in=recommendHistoryList), fields=('uid','username','avatar','location'))
    return HttpResponse(json, mimetype='application/javascript')

