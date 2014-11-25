var imgUrl = '';
var lineLink = '';
var descContent = "测试异性在你心中的排名！";
var shareTitle = '测试异性在你心中的排名,点击试试吧';
var appid = '';
var hasShare=true;

function shareFriend() {
    WeixinJSBridge.invoke('sendAppMessage',{
                            "appid": appid,
                            "img_url": "http://pinlove.com/static/img/pinlove_icon-400_400.png",
                            "img_width": "400",
                            "img_height": "400",
                            "link": lineLink,
                            "desc": descContent,
                            "title": shareTitle
                            }, function(res) {
                            _report('send_msg', res.err_msg);
                            })
}
function shareTimeline() {
    WeixinJSBridge.invoke('shareTimeline',{
                            "img_url": "http://pinlove.com/static/img/pinlove_icon-400_400.png",
                            "img_width": "400",
                            "img_height": "400",
                            "link": lineLink,
                            "desc": descContent,
                            "title": shareTitle
                            }, function(res) {
                            _report('timeline', res.err_msg);
                            });
}
function shareWeibo() {
    WeixinJSBridge.invoke('shareWeibo',{
                            "content": descContent,
                            "url": lineLink,
                            }, function(res) {
                            _report('weibo', res.err_msg);
                            });
}
$(function(){
// 当微信内置浏览器完成内部初始化后会触发WeixinJSBridgeReady事件。
document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
	
	     //页面显示
	      WeixinJSBridge.call('showOptionMenu');
	     

        // 发送给好友
        WeixinJSBridge.on('menu:share:appmessage', function(argv){
            shareFriend();
            });

        // 分享到朋友圈
        WeixinJSBridge.on('menu:share:timeline', function(argv){
            shareTimeline();
            });

        // 分享到微博
        WeixinJSBridge.on('menu:share:weibo', function(argv){
            shareWeibo();
            });
        alert('true')
        }, false);
});