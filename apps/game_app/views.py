#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.game_app.models import Yuanfenjigsaw, YuanfenjigsawWeb
from apps.pay_app.models import  ChargeExchangeRelate
from apps.user_score_app.models import  UserScoreExchangeRelate
import logging
from apps.user_app.models import UserProfile


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
    args={}
    userId=request.user.id
    userProfile=UserProfile.objects.get(user_id=userId)
    from apps.game_app.models import get_recommend_history_web
    facebookUserListDcit=get_recommend_history_web(userId)
    from apps.pay_app.method import get_charge_vailAmount
    from apps.user_score_app.method import get_valid_score
    args={'pinLoveIcon':get_valid_score(userId)+get_charge_vailAmount(userId),'facebookUserListDcit':facebookUserListDcit}
    from pinloveweb.method import init_person_info_for_card_page
    args.update(init_person_info_for_card_page(userProfile))
    from pinloveweb.method import get_no_read_web_count
    args.update(get_no_read_web_count(request.user.id))
    return render(request, 'pintu.html',args)

@csrf_exempt
def jigsaw_web(request):
    match_result = YuanfenjigsawWeb(request.user,filter=request.REQUEST.get('filter'),type=request.REQUEST.get('type')).get_match_result()
    json=simplejson.dumps(match_result)
    return HttpResponse(json, mimetype='application/javascript')

'''
判断积分拼爱币是都足够消费缘分拼图
'''
def check_score_and_PLprice_for_pintu(request):
    try:
        args={}
        from apps.pay_app.method import check_score_and_PLprice
        args=check_score_and_PLprice(request.user.id,"pintu")
        json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception as e:
        logging.error('%s%s'%('check_score_and_PLprice_for_pintu,出错原因：',e))

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
        invite_count=get_invite_count(offset)+1
        #添加到今天推荐过的Uid
        from apps.game_app.models import add_invite_in_day
        add_invite_in_day(uid,offset)
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
备份拼图游戏
'''
def backup_pintu_cache(request):
    from util.cache import backup_cache
    backup_cache('PINTU')
    json=simplejson.dumps({'result':'success'})
    return HttpResponse(json, mimetype='application/javascript')

def restore_backup_pintu_cache(request):
    time=request.GET.get('time')
    from util.cache import restore_backup_cache
    restore_backup_cache('PINTU',time)
    json=simplejson.dumps({'result':'success'})
    return HttpResponse(json, mimetype='application/javascript')

def add_user_count(request):
    count=int(request.GET.get('count'))
    userid=request.GET.get('userid')
    from apps.game_app.models import set_count
    set_count(userid,count)
    json=simplejson.dumps({'result':'success'})
    return HttpResponse(json, mimetype='application/javascript')

def invite_in_day(request):
    userId=request.GET.get('userId')
    from django.core.cache import cache
    inviteInDay= cache.get('INVITE_IN_DAY')
    inviteInDay[userId]=[]
    cache.set('INVITE_IN_DAY',inviteInDay)
    json=simplejson.dumps({'result':'success'})
    return HttpResponse(json, mimetype='application/javascript')
def tset_match(request):
    sql='''
    SELECT DISTINCT name from facebook_user_info where user_id='M2345620' and `name` LIKE BINARY %s
'''
    from util.connection_db import connection_to_db
    match_result=connection_to_db(sql,('%北大%'))
#    callback = request.GET.get('callback')
#    match_result=["2", [0, 1, 4, 5, 6], {"username": "Jin  Snail", "city": "Hangzhou, China", "game_count": 12, "uid": "100007203789389", "facebookPhotoList": "[{\"pk\": \"1401716753411771\", \"model\": \"third_party_login_app.facebookphoto\", \"fields\": {\"bigPhoto\": \"https://scontent-a.xx.fbcdn.net/hphotos-ash3/t1.0-9/1622000_1401716753411771_999418056_n.jpg\", \"smailPhoto\": \"https://fbcdn-photos-e-a.akamaihd.net/hphotos-ak-ash3/t1/1622000_1401716753411771_999418056_s.jpg\", \"user\": \"100007203789389\", \"description\": \"\"}}, {\"pk\": \"1402746386642141\", \"model\": \"third_party_login_app.facebookphoto\", \"fields\": {\"bigPhoto\": \"https://scontent-a.xx.fbcdn.net/hphotos-prn1/t1.0-9/s720x720/1497566_1402746386642141_544486113_n.jpg\", \"smailPhoto\": \"https://fbcdn-photos-g-a.akamaihd.net/hphotos-ak-prn1/t1/1497566_1402746386642141_544486113_s.jpg\", \"user\": \"100007203789389\", \"description\": \"penguin\"}}, {\"pk\": \"1412908328959280\", \"model\": \"third_party_login_app.facebookphoto\", \"fields\": {\"bigPhoto\": \"https://scontent-a.xx.fbcdn.net/hphotos-ash3/t1/1904078_1412908328959280_1054220465_n.jpg\", \"smailPhoto\": \"https://fbcdn-photos-a-a.akamaihd.net/hphotos-ak-ash3/t1/1904078_1412908328959280_1054220465_s.jpg\", \"user\": \"100007203789389\", \"description\": \"\"}}, {\"pk\": \"1412908335625946\", \"model\": \"third_party_login_app.facebookphoto\", \"fields\": {\"bigPhoto\": \"https://scontent-b.xx.fbcdn.net/hphotos-prn2/t1/1656267_1412908335625946_1404365753_n.jpg\", \"smailPhoto\": \"https://fbcdn-photos-b-a.akamaihd.net/hphotos-ak-prn2/t1/1656267_1412908335625946_1404365753_s.jpg\", \"user\": \"100007203789389\", \"description\": \"\"}}, {\"pk\": \"1412908342292612\", \"model\": \"third_party_login_app.facebookphoto\", \"fields\": {\"bigPhoto\": \"https://scontent-b.xx.fbcdn.net/hphotos-prn2/t1.0-9/1798191_1412908342292612_583950951_n.jpg\", \"smailPhoto\": \"https://fbcdn-photos-h-a.akamaihd.net/hphotos-ak-prn2/t1.0-0/1798191_1412908342292612_583950951_s.jpg\", \"user\": \"100007203789389\", \"description\": \"\"}}, {\"pk\": \"1412908362292610\", \"model\": \"third_party_login_app.facebookphoto\", \"fields\": {\"bigPhoto\": \"https://scontent-a.xx.fbcdn.net/hphotos-prn2/t1.0-9/1796596_1412908362292610_1486033668_n.jpg\", \"smailPhoto\": \"https://fbcdn-photos-c-a.akamaihd.net/hphotos-ak-prn2/t1/1796596_1412908362292610_1486033668_s.jpg\", \"user\": \"100007203789389\", \"description\": \"\"}}]", "smallAvatar": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.50.50/p50x50/1622000_1401716753411771_999418056_t.jpg", "age": 24, "avatar": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t1/c0.0.80.80/p80x80/1622000_1401716753411771_999418056_a.jpg"}]
    json=simplejson.dumps(match_result)
    return HttpResponse(json)