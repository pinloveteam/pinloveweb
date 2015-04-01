;(function($, window, document) {
	var loading = $('<div><div><small>正在加载，请稍候...</small></div></div>');
	loading.css('text-align','center').find('div').css({
		'display': 'inline-block',
		'background': 'no-repea url(../img/onload.gif)t',
		'line-height': '16px',
		'padding-left': '20px',
});
	$.fn.popLoading = function() {
		this.append(loading);
	};
	$.fn.removeLoading = function() {
		loading.remove();
	};
	$.fn.failLoading = function() {
		loading.find('small').html('加载失败请刷新!')
	};
	
	$.addShade=$.fn.addShade = function(content) {
		var bodyWidth = document.documentElement.clientWidth; 
		var bodyHeight = Math.max(document.documentElement.clientHeight, document.body.scrollHeight); 
		var bgObj = document.createElement("div" ); 
		bgObj.setAttribute( 'id', 'bgDiv323242423' ); 
		bgObj.style.position = "absolute"; 
		bgObj.style.top = "0"; 
		bgObj.style.background = "#000000"; 
		bgObj.style.filter = "progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75" ; 
		bgObj.style.opacity = "0.5"; 
		bgObj.style.left = "0"; 
		bgObj.style.width = bodyWidth + "px"; 
		bgObj.style.height = bodyHeight + "px"; 
		bgObj.style.zIndex = "10000"; //设置它的zindex属性，让这个div在z轴最大，用户点击页面任何东西都不会有反应| 
		if(typeof this=="object"){
			$(bgObj).css('top',this.offset().top+'px');
			$(bgObj).css('left',this.offset().left+'px');
			$(bgObj).css('height',this.height()+ "px");
			//$(bgObj).css('width',this.width()+ "px")
		 }
		document.body.appendChild(bgObj); //添加遮罩 
		var loadingObj = $('<div id="loadingDiv323242423"></div>');
		loadingObj.css({
			'position':"absolute",
			'top':bodyHeight / 2 - 32 + "px",
			'left':bodyWidth / 2 + "px",
			'background':"no-repeat url(../../static/img/onload.gif)",
			'width':"100px",
			'height':"100px",
			'zIndex' : "10000",
			
		});
		if(content!=undefined ){
			contentDiv=$('<span id="loadingDiv323242423">'+content+'</span>');
			contentDiv.css({
				'position':'relative',
				'color':'white',
			  'left': '40px',
			  'top': '5px',
			 ' font-size': 'initial',
			});
			loadingObj.append(contentDiv)
		}
		$('body').append(loadingObj); //添加loading动画- 
	};
	$.removeShade=$.fn.removeShade = function() {
		$( "#loadingDiv323242423").remove(); 
		$( "#bgDiv323242423").remove(); 
	};
	
})(jQuery, window, document, undefined);

