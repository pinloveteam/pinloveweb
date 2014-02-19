#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.game_app.models import Yuanfenjigsaw, get_count


@csrf_exempt
def jigsaw(request):
    match_result = Yuanfenjigsaw(request).get_match_result()
    json=simplejson.dumps(match_result)
    return HttpResponse(json, mimetype='application/javascript')

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
    try:
        freinds=int(offset)
    except Exception:
        args['result']='error'
        args['errorMessage']='转换失败！'
        json=simplejson.dumps(args)
        return HttpResponse(json, mimetype='application/javascript')
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
        from apps.third_party_login_app.models import FacebookUser
#         username=FacebookUser.objects.get(uid=uid).username
#         args['count']=get_count(username)+get_game_count_forever(uid)
    else:
        args['result']='error'
    json=simplejson.dumps(args)
    return HttpResponse(json, mimetype='application/javascript')
        
