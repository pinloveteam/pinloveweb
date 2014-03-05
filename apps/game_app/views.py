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
    username=FacebookUser.objects.get(uid=request.facebook.uid).username
    count = get_count(username)
    return render(request, 'pintu.html',{'count':count})

'''
邀请好友确认，奖励
'''
def confirm_request_life(request):
    args={}
    userUid=request.session['apprequest']
    uid=request.session['uid']
    uidList=simplejson.loads(request.REQUEST.get('uidList',None))
    for offset in uidList:
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
        #添加确认邀请名单
        from apps.third_party_login_app.models import FacebookUser
        from apps.game_app.models import has_invited,add_invite_confirm
        if not has_invited(offset,uid):
            add_invite_confirm(offset,uid)
        inviteConfirm= cache.get('CONFIRM_INVITE')
#         from apps.third_party_login_app.models import FacebookUser
#         username=FacebookUser.objects.get(uid=uid).username
#         args['count']=get_count(username)+get_game_count_forever(uid)
    args['result']='success'
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
    json=simplejson.dumps({'boys':boys,'boys':girls})
    return HttpResponse(json)

'''
匹配记录
'''
def recommend_history(request):
    uid=request.session['uid']
  
    return HttpResponse(json, mimetype='application/javascript')

'''
备份拼图游戏
'''
def backup_pintu_cache(request):
    from util.cache import backup_cache
    backup_cache('PINTU')
    json=simplejson.dumps({'result':'success'})
    return HttpResponse(json, mimetype='application/javascript')


