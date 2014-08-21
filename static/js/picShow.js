(function($) {
	// 获取路径
//	var path = (function (script) {
//		script = script[script.length-1].src.replace(/\\/g, '/');
//		return script.lastIndexOf('/') < 0 ? '.' : script.substring(0, script.lastIndexOf('/'));
//	})(document.getElementsByTagName('script'));
	
//	$(function () {
//		var cursorCss = ".actizPicShow .bigcursor{cursor:url('" + path + "/images/big.cur'), pointer;}\
//			.actizPicShowExpand .smallcursor{ cursor:url('" + path + "/images/small.cur'), pointer;}\
//			.actizPicShowExpand .leftcursor{ cursor:url('" + path + "/img/pic_prev.cur'), pointer;}\
//			.actizPicShowExpand .rightcursor{ cursor:url('" + path + "/img/pic_next.cur'), pointer;}\
//			}"; //IE cursor 路径相对于HTML
		
//		// link
//		$(document.createElement('link')).attr({
//			href: path + "/picShow.css",
//			rel: "stylesheet",
//			type: "text/css"
//		}).appendTo('head');
//		
//		// style
//		var style = document.createElement('style');
//		style.setAttribute('type', 'text/css');
//		style.styleSheet && (style.styleSheet.cssText += cursorCss) || style.appendChild(document.createTextNode(cursorCss));
//		document.getElementsByTagName('head')[0].appendChild(style);
//		style = null;
//	});
	
	jQuery.fn.actizPicShow=function(option){
		option.id=option.id || $(this).attr("id") ;
		option.width=option.width || 80;//多图片显示宽度
		option.height=option.height || 80;//多图片显示高度
		option.smallWidth=option.smallWidth || 52;
		option.smallHeight=option.smallHeight || 52;
		option.oneWidth=option.oneWidth || 120;//单个图片显示宽度
		option.oneHeight=option.oneHeight || 120;//单个图片显示高度
		option.bigWidth=option.bigWidth || 480; //大图片显示宽度
		option.bigHeight=option.bigHeight || 550;//大图片显示高度
		option.rowSize=option.rowSize || 4;//每行显示多少个
		option.data=option.data || {};//图片数组   id img bigimg middleimg
		if(option.id==null || option.id==''){
			$(this).attr("id",new Date().getTime());
			option.id=$(this).attr("id");
		}
		$(this).children().remove();//清楚该id 下所有的元素。。。
		var me=$(this);
		var current_i=0;//当前中间显示的图片在数组中的位置 important
		var currentPage=1;//底下小图片当前第几页
		var currentPageSize=Math.ceil(option.data.length/7);//总共多少页
		var morePic=false;
		if(option.data.length>1){
			morePic=true;
		}else if(option.data.length==0){
			return;
		}
		if(morePic){
			expandMorePicShow();
		}else{
			expandOnePicShow();
		}
//		function narrowMorePicShow(){//多图片 小图片显示
//			var _picshow_narrow_exist=me.find("#"+option.id+"_picshow_narrow");
//			if(_picshow_narrow_exist.size()>0){
//				_picshow_narrow_exist.show();
//				return;
//			}
//			var morepicArray= new Array();
//			morepicArray.push('<div id="'+option.id+'_picshow_narrow" class="actizPicShow">');
//			morepicArray.push('<ul>');
//			for(var i=0;i<option.data.length;i++){
//				morepicArray.push('<li>');
//				morepicArray.push('<img id="'+option.data[i].id+'" height="'+option.height+'px" width="'+option.width+'px" class="bigcursor" curLoc="'+i+'" ');
//				morepicArray.push('src="'+option.data[i].img+'" alt="">');
//				morepicArray.push('</li>');
//			}
//			morepicArray.push('</ul>');
//			morepicArray.push('</div>');
//			$("#" +option.id).append(morepicArray.join(""));
//			var _picshow_narrow=$("#" +option.id+"_picshow_narrow");
//			_picshow_narrow.css("width",((option.width+6)*option.rowSize+45)+"px");
//		}

		function expandMorePicShow(){//多图片 大图片显示
			var _picshow_expand_exist=me.find("#"+option.id+"_picshow_expand");
			if(_picshow_expand_exist.size()>0){
				getCurrentPicChange();
				expandCenterUpdate();
				_picshow_expand_exist.show();
				return;
			}
			var b=new Array();
			b.push('<div id="'+option.id+'_picshow_expand" class="actizPicShowExpand">');
//			b.push(expandTop());
			b.push(expandCenterImgHtml(option.data[current_i].id,option.data[current_i].middleimg));
			b.push(expandFootMoreHtml());
			b.push('</div>');
			$("#" +option.id).append(b.join(""));
			$("#" +option.id+"_picshow_expand").css("width",option.bigWidth+"px");
//			expandAddDavFile();
			getCurrentPicChange();
		}
//		function narrowOnePicShow(){//单个图片 小图片显示
//			var _picshow_narrow_exist=me.find("#"+option.id+"_picshow_narrow");
//			if(_picshow_narrow_exist.size()>0){
//				_picshow_narrow_exist.show();
//				return;
//			}
//			var onepicArray= new Array();
//			onepicArray.push('<div id="'+option.id+'_picshow_narrow" class="actizPicShow">');
//			onepicArray.push('<img id="'+option.data[0].id+'" class="bigcursor" curLoc="0" ');
//			onepicArray.push('src="'+option.data[0].img+'" alt="">');
//			onepicArray.push('</div>');
//			me.append(onepicArray.join(""));
//		}

		function expandOnePicShow(){//单个图片 大图片 显示
			var _picshow_expand_exist=me.find("#"+option.id+"_picshow_expand");
			if(_picshow_expand_exist.size()>0){
//				expandAddDavFile();
				_picshow_expand_exist.show();
				return;
			}
			var b=new Array();
			b.push('<div id="'+option.id+'_picshow_expand" class="actizPicShowExpand">');
			//b.push(expandTop());
			b.push(expandCenterImgHtml(option.data[0].id,option.data[0].middleimg));
			b.push('</div>');
			$("#" +option.id).append(b.join(""));
			$("#" +option.id+"_picshow_expand").css("width",option.bigWidth+"px");
//			expandAddDavFile();
		}

//		function expandTop(){
//			var a=new Array();
//			a.push('<p class="expand_top">');
//			a.push('<a  href="javascript:void(0);" class="retract" ><em class="W_ico12 ico_retract" style="float: inherit;"></em>收起</a>');
//			a.push('<i class="W_vline">|</i>');
//			a.push('<a href="javascript:;" class="showbig"><em class="W_ico12 ico_showbig" style="float: inherit;"></em> 查看原图</a>');
//			a.push('<i class="W_vline">|</i>');
//			a.push('<a  href="javascript:void(0);" class="turn_left" ><em class="W_ico12 ico_turnleft" style="float: inherit;"></em> 向左转</a>');
//			a.push('<i class="W_vline">|</i>');
//			a.push('<a href="javascript:void(0);" class="turn_right"><em class="W_ico12 ico_turnright" style="float: inherit;"></em> 向右转</a>');
//			a.push('<i class="W_vline">|</i>');
//			//a.push('<a href="javascript:void(0);" class="collect"><em class="W_ico12 ico_collect"></em> 收藏</a>');
//			a.push('</p>');
//			return a.join("");
//		}
		function expandCenterImgHtml(id , img){
			var c=new Array();
			c.push('<div id="expandCenterImg">');
			c.push('<img  src="'+img+'" id="'+id+'" class="centerImg">');
			c.push('</div>');
			return c.join("");
		}
		function expandFootMoreHtml(){
			var d=new Array();
			d.push('<div id="pic_choose_box" class="pic_choose_box">');
			d.push('<a href="javascript:;"  class="arrow_left_small" title="上一页"><em class="ico_pic_prev">&lt;</em></a>');
			d.push('<div class="stage_box">');
			d.push('<ul>');
			for(var i=0;i<option.data.length;i++){
				d.push('<li>');
				d.push('<a href="javascript:;" curLoc="'+i+'">');
				d.push('<img id="'+option.data[i].id+'" height="'+option.smallWidth+'px" width="'+option.smallHeight+'px" class="cursor" ');
				d.push('src="'+option.data[i].img+'" alt="">');
				d.push('</a>');
				d.push('</li>');
			}
			d.push('</ul>');
			d.push('</div>');
			d.push('<a href="javascript:;"  class="arrow_right_small" title="下一页"><em class="ico_pic_next">&gt;</em></a>');
			d.push('</div>');
			return d.join("");
		}
		/**
		 * 多图片中间图片改变时的方法
		 */
		function expandCenterUpdate(){
//			expandAddDavFile();
			var expandCenterImg=me.find("#expandCenterImg");
			var c=new Array();
			c.push('<img  src="'+option.data[current_i].middleimg+'" id="'+option.data[current_i].id+'" class="centerImg">');
			expandCenterImg.children().remove();
			expandCenterImg.append(c.join(""));
			expandCenterImg.css("height","auto");
		}
		/**
		 * 收藏
		 */
//		function expandAddDavFile(){
//			var expandTop=$("#" +option.id+"_picshow_expand").find(".expand_top");
//			var fav=$('<a href="javascript:;" class="addFavFile archivebtn" id="addFavFile_'+option.data[current_i].id+'" style="margin: -5px;"></a>');
//			expandTop.find(".addFavFile").remove();
//			expandTop.append(fav);
//		}
		/**
		 * 进入多图片大图时方法
		 */
		function getCurrentPicChange(){
			currentPage=Math.ceil((parseInt(current_i)+1)/7);//当前第几页
			changeCurrentPage();
			var stage_boxa=me.find("#pic_choose_box .stage_box");
			stage_boxa.find("a").each(function(i){
				$(this).removeClass("current");
				if(current_i==i){
					$(this).addClass("current");
				}
			});
		}
		/**
		 * 当前页面改变时  ------底下的图片改变样式
		 */
		function changeCurrentPage(){
			var arrow_right_small=me.find(".arrow_right_small");
			var arrow_left_small=me.find(".arrow_left_small");
			var ico_pic_prev=me.find(".ico_pic_prev");
			var ico_pic_next=me.find(".ico_pic_next");
			if(currentPage>1){
				arrow_left_small.removeClass("big2").addClass("big1");
				ico_pic_prev.removeClass("text2").addClass("text1");
			}else{
				arrow_left_small.removeClass("big1").addClass("big2");
				ico_pic_prev.removeClass("text1").addClass("text2");
			}
			if(currentPage>=currentPageSize){
				arrow_right_small.removeClass("big1").addClass("big2");
				ico_pic_next.removeClass("text1").addClass("text2");
			}else{
				arrow_right_small.removeClass("big2").addClass("big1");
				ico_pic_next.removeClass("text2").addClass("text1");
			}
			var stage_box_ul=me.find("#pic_choose_box .stage_box ul");
			var marginleft=(currentPage-1)*59*7;
			stage_box_ul.css("margin-left","-"+marginleft+"px");
		}
		//当最大化的时候事件绑定----收起
//		me.delegate(".retract","click",function(){
//			me.find("#"+option.id+"_picshow_narrow").show();
//			me.find("#"+option.id+"_picshow_expand").hide();
//		});
		//当最大化的时候事件绑定----原图
//		me.delegate(".showbig","click",function(){
//			window.open(option.data[current_i].bigimg);
//		});
		//当最大化的时候事件绑定----向左旋转
//		me.delegate(".turn_left","click",function(){
//			me.find("#expandCenterImg .centerImg").rotateLeft(option.bigWidth-44);
//		});
		//当最大化的时候事件绑定----向右旋转
//		me.delegate(".turn_right","click",function(){
//			me.find("#expandCenterImg .centerImg").rotateRight(option.bigWidth-44);
//		});
		//当最大化的时候事件绑定----起
//		me.delegate(".smallcursor","click",function(){
//			me.find("#"+option.id+"_picshow_expand").hide();
//			me.find("#"+option.id+"_picshow_narrow").show();
//		});
		//当最大化的时候事件绑定----收藏
		//me.delegate(".collect","click",function(){
		//	console.log("this pic id is :"+option.data[current_i].id);
		//});
		//当最大化的时候事件绑定----上一个
		me.delegate(".leftcursor","click",function(){
			if(current_i==0)return;
			current_i-=1;
			expandMorePicShow();
		});
		//当最大化的时候事件绑定----下一个
		me.delegate(".rightcursor","click",function(){
			if(current_i==option.data.length-1)return;
			current_i+=1;
			expandMorePicShow();
		});
		//当最大化的时候事件绑定----上一页
		me.delegate(".arrow_left_small","click",function(){
			if(currentPage==1)return;
			currentPage=currentPage-1;
			changeCurrentPage();
		});
		//当最大化的时候事件绑定----下一页
		me.delegate(".arrow_right_small","click",function(){
			if(currentPage>=currentPageSize)return;
			currentPage=currentPage+1;
			changeCurrentPage();
		});
		//大图时 绑定 移动事件
		me.delegate("#expandCenterImg","mousemove",function(e){
			if(morePic==false){
				$(this).addClass("smallcursor");
				return;
			}
			var x= e.clientX;
			var left=$(this).offset().left;
			var switchWidth=x-left;
			if(switchWidth<120 && current_i!=0){
				$(this).removeClass("smallcursor").removeClass("rightcursor").addClass("leftcursor");
			}else if(switchWidth<=440 && switchWidth>=320 && current_i!=option.data.length-1){
				$(this).removeClass("leftcursor").removeClass("smallcursor").addClass("rightcursor");
			}else if(switchWidth<=440){
				$(this).removeClass("leftcursor").removeClass("rightcursor").addClass("smallcursor");
			}else{
				$(this).removeClass("leftcursor").removeClass("rightcursor").removeClass("smallcursor");
			}
		});
		
		//大图时底下小图事件绑定
		me.delegate(".stage_box a","click",function(){
			var curLoc=parseInt($(this).attr("curLoc"));
			current_i=curLoc;
			expandCenterUpdate();
			me.find(".stage_box a").removeClass("current");
			$(this).addClass("current");
		});
		//小图片放大事件
//		me.delegate(".bigcursor","click",function(e){
//			var curLoc=parseInt($(this).attr("curLoc"));
//			current_i=curLoc;
//			var _picshow_narrow=$("#" +option.id+"_picshow_narrow");
//			_picshow_narrow.hide();
//			if(morePic){
//				expandMorePicShow();
//			}else{
//				expandOnePicShow();
//			}
//			
//		});
		//绑定图片收藏事件....
//		me.delegate(".bigcursor","mouseover",function(e){
//			var curLoc=parseInt($(this).attr("curLoc"));
//			me.find(".addFavFile").remove();
//			var addFav=$('<a href="javascript:" class="addFavFile archivebtn" id="addFavFile_'+option.data[curLoc].id+'"></a>');
//			if(morePic){
//				addFav.css("left","1px");
//				addFav.css("position","absolute");
//			}
//			$(this).after(addFav);
//		});
		
	};
	
})($);
