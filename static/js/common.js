function is_PC(){
	//平台、设备和操作系统
	var system ={
	win : false,
	mac : false,
	xll : false
	};
	//检测平台
	var p = navigator.platform;
	system.win = p.indexOf("Win") == 0;
	system.mac = p.indexOf("Mac") == 0;
	system.x11 = (p == "X11") || (p.indexOf("Linux") == 0);
	//跳转语句
	if(system.win||system.mac||system.xll){
	return true;
	}else{
		return false;
	}
}
//从Cookie获得信息
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//获取url参数
function get_url_param(param){
	var paramStr=window.location.search+'&';
	result=false;
	reString=param+'=(.*?)&'
	 re =new RegExp(reString);
	 r=paramStr.match(re)
	 if(r!=null){
		 result=r[1];
	 }
	return result;
}