var datasets_self = {fillColor : "rgba(0,0,0,0)",strokeColor : "rgb(0,151,36)",pointColor : "rgb(0,151,36)"}
var datasets_other = {fillColor : "rgba(0,0,0,0)",strokeColor : "rgb(241,23,25)",pointColor : "rgb(241,23,25)"}
var comparable = false;
var name_self , name_other , showedRadar;
var dataArray = {};
detail_info=true;
var compare_flag=false;
//选择用户
var check_id=null;
var diaogList=[];
window.Card = function(person){
	var test_match= function(){
			var userId=$(this).parent().attr("id")
			userId=userId.substring(4,userId.length)
			$.ajax({
				url:'/recommend/test_match/',
				data:{userId:userId},
				dataType:"json",
				success:function(data){
					alert(JSON.stringify(data))
				}
			});
	}
	var dislike = function(){
		var userId=$(this).parents('.card').attr('id');
		var temp=$(this)
	    $.getJSON("/user/dislike/",{userId:userId,page:next_page_number-1},function(data) {
		  if(data['result']=='success'){
			 temp.parents('.card').hide('slow');
			 card=data['card'];
			 var avatar_name='/media/'+card.avatar_name;
			 new Card(new Person(card.username,card.age,card.city,avatar_name,card.user_id,card.isFriend));
			 if (data['has_next']){
			 }else{
				 next_page_number=-1;
				 $('.next').hide();
			 }
		 }else if(data['result']=='remove_card'){
			temp.parents('.card').hide('slow');
		 }
	 });
	 venobox();
	}
	
	var like= function(){
	    var userId=$(this).parents('.card_panel').attr('id');
		var icon_like=$(this).parents('.tool_bar :nth-child(2) ').children();
		$.getJSON("/user/update_follow/",{userId:userId},function(data) {
			  if(data['type']==1){
					icon_like.removeClass().addClass("icon_like_1")
					myFollow=myFollow+1
					$('#myFollow').html(myFollow)
			  }else if(data['type']==2){
				  icon_like.removeClass().addClass("icon_like_2")
					follow=follow+1
					myFollow=myFollow+1
					$('#follow').html(follow)
					$('#myFollow').html(myFollow)
				  }else{
					  icon_like.following();
				     if(data['type']==-1){
				    	 icon_like.removeClass().addClass("icon_like_0") 
				    	 myFollow=myFollow-1
					     $('#myFollow').html(myFollow)
				     }else{
				    	 icon_like.removeClass().addClass("icon_like_3") 
				    	 follow=follow-1
						 myFollow=myFollow-1
						 $('#follow').html(follow)
						 $('#myFollow').html(myFollow)
				     }
				     
				  };
		       
		       
		    });
	};
	
	//初始化对话框
	var init_msg = function(){
	    panel = $(this).parents('.card-nav').prev().find('.chat');
    	 panel.jScrollPane();
    	  var userId=$(this).parents('.card_panel').attr('id');
    	   $.getJSON("/message/get_noread_messges/",{userId:userId,ajax:true},function(data) {
    		   if (data['login']=='invalid'){
    			   alert("请先登录");
    			   window.location =data['redirectURL'];
    		   }
    		   panel.children().children().children().remove();
    		   for(var message in data){
    			   if (userId!=data[message].receiver_id){
    				   var api = panel.data('jsp');
    					var chat = panel.find('.jspPane');
    					chat.append('<div class="chat_content_group other"><div class="chat_content">'+data[message].content+'<div class="cloudArrow "></div></div></div>');
    					panel.jScrollPane();
    					api.scrollTo(0,9999);
    			   }else{
    				   var api = panel.data('jsp');
    				    var chat = panel.find('.jspPane');
    					chat.append('<div class="chat_content_group self"><div class="chat_content">'+data[message].content+'<div class="cloudArrow "></div></div></div>');
    					panel.jScrollPane();
    					api.scrollTo(0,9999);
    			   }
    	    	  
    	      }
    	   });	
	};
	
	var ding = function(){
		$(this).toggleClass('ding').hasClass('ding')?$(this).attr('title','取消固定').parents('.card').removeClass('hideable'):$(this).attr('title','固定').parents('.card').addClass('hideable');
	}
	
	var sendMsg = function(){
		var api = pane.data('jsp');
		var content = $(this).prev();
		var chat = $(this).prevAll('.chat').find('.jspPane');
		var send_content = content.val().trim();
		var receiver_id=$(this).parents('.card_panel').attr('id');
		if(send_content!=''){
		   $.getJSON('/message/send/',{receiver_id:receiver_id,reply_content:send_content},function(data){
			  chat.append('<div class="chat_content_group self"><div class="chat_content">'+send_content+'<div class="cloudArrow"></div></div></div>');
			  content.val('');
			  pane.jScrollPane();
		      api.scrollTo(0,9999);
		  });
	}
		
	}
	
	var showRadar = function(event){
		var mouse_x = event.pageX;
		if(this.isRadarShow){
		$(this).children().not('.name').hide('fast');
			this.isRadarShow = false;
		}
		else{
			current=$(this)
			userId=current.closest('.card_panel').attr('id')
			username=current.find('.username').html()
			if (dataArray[username]==null){
				$.ajax({
					type:'GET',
					url:'/recommend/get_socre_for_other/',
					dataType:"json",
					data:{userId:userId},
					success:function(data, textStatus){
						if(textStatus=='success'){
							if(data['result']=='success'){
								matchResult=data['matchResult']
								dataArray[username]= [matchResult.heighScore,matchResult.incomeScore,matchResult.edcationScore,matchResult.appearanceScore,matchResult.characterScore,];
								current.find('#my_score_other').html('总分：'+matchResult.scoreOther.toString()+'分')
								if(matchResult.scoreMyself){
									current.find('.other_score_my').remove()
									current.find('.dafen').append('<div id="scoreMyself">她对你的打分：'+matchResult.scoreMyself+'分</div>')
								}
								
								if(showedRadar){
									$(showedRadar).children().not('.name').hide('fast');
									showedRadar.isRadarShow = false;
								}
								
								if(mouse_x>1000){
									current.find("canvas").css('left','-100px');
									current.find(".radar").css('left','-210px');
								}
								current.find("canvas").show('fast');
								var ctx = current.find("canvas").get(0).getContext("2d");
								current.find(".radar").show('fast');
								var name = current.attr('title');
								datasets_self.data = dataArray[name];
								var data = {labels : labels, datasets : [datasets_self]};
								var myNewChart = new Chart(ctx).Radar(data,{scaleOverride:true,scaleSteps:4,scaleStepWidth:25,scaleStartValue:0,scaleLineColor : "rgba(0,0,0,.5)",scaleShowLabels : true,angleLineColor : "rgba(0,0,0,.5)"});
								current.isRadarShow = true;
								showedRadar = current;
								
							}else if(data['result']=='error'){
								alert(data['error_messge'])
							}
							
						}
					},
					error:function(response){
						alert('网络异常!')
					},
			});
			}else{
				if(showedRadar){
					$(showedRadar).children().not('.name').hide('fast');
					showedRadar.isRadarShow = false;
				}
				
				if(mouse_x>1000){
					$(this).find("canvas").css('left','-100px');
					$(this).find(".radar").css('left','-210px');
				}
				$(this).find("canvas").show('fast');
				var ctx = $(this).find("canvas").get(0).getContext("2d");
				$(this).find(".radar").show('fast');
				var name = $(this).attr('title');
				datasets_self.data = dataArray[name];
				var data = {labels : labels, datasets : [datasets_self]};
				var myNewChart = new Chart(ctx).Radar(data,{scaleOverride:true,scaleSteps:4,scaleStepWidth:25,scaleStartValue:0,scaleLineColor : "rgba(0,0,0,.5)",scaleShowLabels : true,angleLineColor : "rgba(0,0,0,.5)"});
				this.isRadarShow = true;
				showedRadar = this;
			}
			
			
		}
	}
	
	
/*	var compareRadar = function(){
		if(this.isRadarShow){
			$(this).children().not('.name').hide('fast');
			this.isRadarShow = false;
		}
		else{
			current=$(this)
			userId=current.closest('.card_panel').attr('id')
			username=current.find('.username').html()
			if (dataArray[username]==null){
				$.ajax({
					type:'GET',
					url:'/recommend/get_socre_for_other/',
					dataType:"json",
					data:{userId:userId},
					success:function(data, textStatus){
						if(textStatus=='success'){
							if(data['result']=='success'){
								matchResult=data['matchResult']
								dataArray[username]= [matchResult.heighScore,matchResult.incomeScore,matchResult.edcationScore,matchResult.appearanceScore,matchResult.characterScore,];
								current.find('#my_score_other').html('总分：'+matchResult.scoreOther.toString()+'分')
								if(matchResult.scoreMyself){
									current.find('.other_score_my').remove()
									current.find('.dafen').append('<div id="scoreMyself">她对你的打分：'+matchResult.scoreMyself+'分</div>')
								}
								
								current.find("canvas").show('fast');
								var ctx = current.find("canvas").get(0).getContext("2d");
								current.find(".radar").show('fast');
								current.find(".compare").hide('fast');
								current.find(".compare_cancle").show('fast');
								current.find(".chart_info").show('fast')
								name_other = current.attr('title');
								datasets_self.data = dataArray[name_self];
								datasets_other.data = dataArray[name_other];
								var data = {labels : labels, datasets : [datasets_other,datasets_self]};
								var myNewChart = new Chart(ctx).Radar(data,{scaleOverride:true,scaleSteps:4,scaleStepWidth:25,scaleStartValue:0,scaleLineColor : "rgba(0,0,0,.5)",angleLineColor : "rgba(0,0,0,.5)"});
								if(name_self!=name_other){
									current.find(".chart_info").find(".name_self").html(name_self);
									current.find(".chart_info").find(".name_other").html(name_other);
								}
								else{
									current.find(".chart_info").find(".name_self").html('');
									current.find(".chart_info").find(".name_other").html('');
								}
								this.isRadarShow = true;
								showedRadar = this;
								
							}else if(data['result']=='error'){
								alert(data['error_messge'])
							}
							
						}
					},
					error:function(response){
						alert('网络异常!')
					},
			});
			}else{
				if(showedRadar){
					$(showedRadar).children().not('.name').hide('fast');
					showedRadar.isRadarShow = false;
				}
				
				$(this).find("canvas").show('fast');
				var ctx = $(this).find("canvas").get(0).getContext("2d");
				$(this).find(".radar").show('fast');
				$(this).find(".compare").hide('fast');
				$(this).find(".compare_cancle").show('fast');
				$(this).find(".chart_info").show('fast')
				name_other = $(this).attr('title');
				datasets_self.data = dataArray[name_self];
				datasets_other.data = dataArray[name_other];
				var data = {labels : labels, datasets : [datasets_other,datasets_self]};
				var myNewChart = new Chart(ctx).Radar(data,{scaleOverride:true,scaleSteps:4,scaleStepWidth:25,scaleStartValue:0,scaleLineColor : "rgba(0,0,0,.5)",angleLineColor : "rgba(0,0,0,.5)"});
				if(name_self!=name_other){
					$(this).find(".chart_info").find(".name_self").html(name_self);
					$(this).find(".chart_info").find(".name_other").html(name_other);
				}
				else{
					$(this).find(".chart_info").find(".name_self").html('');
					$(this).find(".chart_info").find(".name_other").html('');
				}
				this.isRadarShow = true;
				showedRadar = this;
			}
			
		}
	}
	
	var compare = function(){
		$(this).parents('.card').addClass('chosen');
		$('.compare').hide();
		$('.compare_cancle').show('fast');
		name_self = $(this).parent().parent().attr('title');
		$('#compare_tip').show('slow',function(){
			$(this).delay(2000).hide('slow');
		});
		comparable = true;
		
		$('.other_name').unbind();
		$('.other_name').on('click',compareRadar);
	}*/
	
	/*创建雷达图
	data[list]*/
	function create_dialog(data){
		dialog=$('.poplayer')
		var ctx = dialog.find('canvas').get(0).getContext("2d");
		var datasets = {
			fillColor : "rgba(0,0,0,0)",
			strokeColor : "rgb(0,151,36)",
			pointColor : "rgb(0,151,36)",
			data:data
		}
		var data = {
				labels : ["教育程度", "性格", "收入情况", "样貌", "身高"],
				datasets : [datasets]
			};
		var myNewChart = new Chart(ctx).Radar(data, {
			scaleOverride : true,
			scaleSteps : 4,
			scaleStepWidth : 25,
			scaleStartValue : 0,
			scaleLineColor : "rgba(0,0,0,.5)",
			scaleShowLabels : true,
			angleLineColor : "rgba(0,0,0,.5)"
		});
		return dialog;
	}
	var compare_cancle = function(){
		$('.chosen').removeClass('chosen');
		$('.compare').show();
		$('.compare_cancle').hide('fast');
		comparable = false;
		name_other = '';
		name_self = '';
		
		$('.other_name').unbind();
		$('.other_name').on('click',showRadar);
	}
	
    
	var score_my = function(e){
		current=$(this)
		userId=$(this).val()
		e.stopPropagation();    //  阻止事件冒泡
		$.ajax({
				type:'GET',
				url:'/recommend/socre_my/',
				dataType:"json",
				data:{userId:userId},
				success:function(data, textStatus){
					if(textStatus=='success'){
						if(data['result']=='success'){
							current.parent().append(data['scoreMyself'])
							current.remove()
						}else if(data['result']=='error'){
							alert(data['error_messge'])
						}
						
					}
				},
				error:function(response){
					alert('网络异常!')
				},
		});
	}
	
	/*type:
		1---对比
		2--取消对比*/
	function compare(userId,type,guide=false){
		if(type==1){
			compare_flag=true;
			check_id=userId;
		}else{
			compare_flag=false;
		}
		
		//引导
		if(guide){
			introBox=$('.card_row').children().not('#'+userId).first().find('.card-introBox')
			if(introBox.length){
				introBox.attr('id','compare_img')
			}
			 var tour = {
						id : "hello-hopscotch",
						steps : [{
							title : "对比信息",
							content : "点击头像就可以进行信息对比",
							target : 'compare_img',
							placement : "top"
						}]
					};
			 
			hopscotch.startTour(tour);
		 }
	}
	
	//对比用户中的取消对比
	function cancel_compare(userId){
		$('.compare-btn_1').closest('.col-xs-4').remove();
		$('.compare-btn').html('对比');
		$('.score_other').remove();
		dialog=create_dialog(diaogList);
		$('.poplayer').css('left','25%').css('width','780px');
		 $('.compare-btn').click(function(){compare(userId,1)})
	}
	
	//生成个人详细信息页面，对比页面
	function detail_info(){
		context=this
		if ( $('.masklayer').length==0&&detail_info){
		detail_info=false;
		userId=$(this).closest('.card').attr('id');
		if(compare_flag){
			if(check_id==userId){
				detail_info=true;
				var body = $("<p>不能选择同一个用户!</p>")
	        	 $.poplayer({body:body});
				 return;
			}
			data={userId:check_id,compareId:userId}
		}else{
			data={userId:userId}
		}
		
		$.ajax({
			type:'GET',
			url:'/user/detailed_info/',
			data:data,
			dataType:"json",
			success:function(data, textStatus){
				try {
				 var body = $(data.detail)
				 var socreForOther=data.socreForOther
				 if(compare_flag){
					 diaogList=[socreForOther.matchResult.edcationScore,socreForOther.matchResult.characterScore,socreForOther.matchResult.incomeScore,socreForOther.matchResult.appearanceScore,socreForOther.matchResult.heighScore,]					 
					 var compareSocreForOther=data.compareSocreForOther
					 compareList=[compareSocreForOther.matchResult.edcationScore,compareSocreForOther.matchResult.characterScore,compareSocreForOther.matchResult.incomeScore,compareSocreForOther.matchResult.appearanceScore,compareSocreForOther.matchResult.heighScore,]
					 $.poplayer({body:body,type:'frame',data:diaogList,data2:compareList});
					 $('.compare-btn').click(function(){
						 compare(userId,2)
					 })
					 
				 }else{
					 guide=false;
					 if(data.socreForOther.result=="success"){
						 diaogList=[socreForOther.matchResult.edcationScore,socreForOther.matchResult.characterScore,socreForOther.matchResult.incomeScore,socreForOther.matchResult.appearanceScore,socreForOther.matchResult.heighScore,]
						 $.poplayer({body:body,type:'frame',data:diaogList,data2:[]});
						 if(data.compare_button){
							 var tour = {
										id : "hello-hopscotch",
										steps : [{
											title : "对比雷达图",
											content : "点击对比，可以对比两个人的个人信息以及雷达图",
											target : "compare-button",
											placement : "top"
										}]
									};
							hopscotch.startTour(tour);
							guide=true;
						 }
						 $('.compare-btn').click(function(){
							 compare(userId,1,guide)
						 });
					 }else{
						 detail_info=true
						 $.poplayer({body:body,type:'error'});
						 $('.compare-btn').attr('disable',true);
						 $('.compare-btn').removeClass('btn-info')
//							var body = $("<p>"+socreForOther.error_messge+"</p>")
//							$.poplayer({body:body});
					 }
					 
				 }
				 $('#radar').find('button').on('click',score_my);
				 $('.compare-btn_1').click(function(){
					 cancel_compare(userId)
				 })
				 detail_info=true;
			 } catch (e) {
					detail_info=true
					var body = $("<p>异常错误!</p>")
					$.poplayer({body:body});
						}
			},
			error:function(response){
				detail_info=true;
				var body = $("<p>网络异常!</p>")
	        	 $.poplayer({body:body});
			},
	});
		}
		
	}
	this.template = $('#card').clone();

	this.template.find('.username').html(person.username);
	this.template.find('.tag').children().first().html(person.age).next().html(person.city);
	this.template.find('.head').children().attr('src',person.headImg+'-110.jpeg');
	this.template.find('.min_head').children().attr('src',person.headImg+'-60.jpeg');
	this.template.find('.card').attr('id',person.username);
	this.template.find('.other_name').attr('title',person.username);
	this.template.find('#dynamic').attr('href','/dynamic/person/?userId='+person.userId);
	//初始化详细信息href
//	this.template.find('.introBox').attr('href','/user/detailed_info/'+person.userId.toString());
    //添加用户id
	this.template.find('.card_panel').attr('id',person.userId);
	//是否关注
	var icon_like=this.template.find('.tool_bar :nth-child(2) ').children();
	icon_like.removeClass().addClass('icon_like_'+person.isFriend);
	icon_like.attr('move-data',person.headImg+'-60.jpeg')
	if(person.isFriend=='0'||person.isFriend=='1'){
		icon_like.attr('move-to','js-follow')
	}else{
		icon_like.attr('move-to','js-follow-each')
	}
	
	//添加tab id
	var tab=this.template.find('.tab-pane');
	var nav=this.template.find('.card-nav').children().children();
	for (i=0;i<3;i++){
      j=i+4
	  tab[i].id='tab'+j+person.userId;
	  nav[i].href='#tab'+j+person.userId;
	}

	for(i=0;i<person.pictureList.length;i++){
		if(i<=6){
			this.template.find('.hoverbox').append('<li><a class="venobox" data-gall="gall1_'+person.userId+'" href="/media/'+person.pictureList[i].pic+'" title="'+person.pictureList[i].description+'"><img alt="demo1" src="/media/'+person.pictureList[i].smailPic+'" title="demo1"></a></li>');
		}else{
			this.template.find('.hoverbox').append('<li><a  style="display:none;" class="venobox" data-gall="gall1_'+person.userId+'" href="/media/'+person.pictureList[i].pic+'" title="'+person.pictureList[i].description+'"><img alt="demo1" src="/media/'+person.pictureList[i].smailPic+'" title="demo1"></a></li>');
		}
	}
		
	$('.card_row').append(this.template.html());
	
	$('.icon_dislike,.icon_ding,.btn_send_msg,[class^="icon_like"],.icon_msg,.test_match,.introBox').unbind();
	
	$('.icon_dislike').on('click',dislike);
	
	$('.icon_ding').on('click',ding);
	
	$('.btn_send_msg').on('click',sendMsg);
	
	$("[class^='icon_like']").on('click',like);
	
	$(".icon_msg").on('click',init_msg);
	$(".test_match").on('click',test_match);
	$('.dafen').find('button').unbind();
	$('.introBox').on('click',detail_info);
	
	$(function(){
		 $('.icon_like_0,.icon_like_3').following();
		});
}

function Person(username,age,city,headImg,userId,isFriend,pictureList){
	this.username = username;
	this.age = age;
	this.city = city;
	this.headImg = headImg;
	this.userId=userId;
	this.isFriend=isFriend;
	this.pictureList=pictureList;
	
}