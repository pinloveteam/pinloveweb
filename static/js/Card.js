var datasets_self = {fillColor : "rgba(0,0,0,0)",strokeColor : "rgb(0,151,36)",pointColor : "rgb(0,151,36)"}
var datasets_other = {fillColor : "rgba(0,0,0,0)",strokeColor : "rgb(241,23,25)",pointColor : "rgb(241,23,25)"}
var comparable = false;
var name_self , name_other , showedRadar;
var dataArray = {};
detail_info=true;
var compare_flag=false;
//选择用户
var check_id=null;
var diaogList={user1:[null,null,null,],user2:null};
var mgr = hopscotch.getCalloutManager();
state = hopscotch.getState();
//判断是不是有card页面
isChard=true;
//分数显示
var Time, i = 0, num, progress, score;


var sendMsg = function(){
	var api = pane.data('jsp');
	var content = $(this).prev();
	var chat = $(this).prevAll('.chat').find('.jspPane');
	var send_content = content.val().trim();
	var receiver_id=$(this).parents('.card_panel').attr('id');
	if(send_content!=''){
	   $.getJSON('/message/send/',{receiver_id:receiver_id,reply_content:send_content},function(data){
		   if(data.result=='success'){
			   chat.append('<div class="chat_content_group self"><div class="chat_content">'+send_content+'<div class="cloudArrow"></div></div></div>');
				content.val('');
				pane.jScrollPane();
			    //api.scrollTo(0,9999);
				chat.parent().animate({scrollTop:9999},100)
		   }else{
			   var body=$('<p>'+data.error_message+'</p>')
			   $.poplayer({body:body});
		   }
		 
	  });
}
	
}

//初始化对话框
//var init_msg = function(){
//    panel = $(this).parents('.card-nav').prev().find('.chat');
//	 panel.jScrollPane();
//	  var userId=$(this).parents('.card_panel').attr('id');
//	   $.getJSON("/message/get_no_read_messge_by_ids/",{userIds:userId},function(data) {
//		   messageBean=data['messageList'][message]
//   	       var api = pane.data('jsp');
//		   panel.children().children().children().remove();
//			var chat = $('#'+messageBean.senderId).find('.jspPane')
//			chat.append('<div class="chat_content_group other"><div class="chat_content">'+messageBean.content+'<div class="cloudArrow "></div></div></div>');
//			pane.jScrollPane();
//			api.scrollTo(0,9999);
//			
//		   if (data['login']=='invalid'){
//			   alert("请先登录");
//			   window.location =data['redirectURL'];
//		   }
//		   panel.children().children().children().remove();
//		   for(var message in data){
//			   if (userId!=data[message].receiver_id){
//				   var api = panel.data('jsp');
//					var chat = panel.find('.jspPane');
//					chat.append('<div class="chat_content_group other"><div class="chat_content">'+data[message].content+'<div class="cloudArrow "></div></div></div>');
//					panel.jScrollPane();
//					api.scrollTo(0,9999);
//			   }else{
//				   var api = panel.data('jsp');
//				    var chat = panel.find('.jspPane');
//					chat.append('<div class="chat_content_group self"><div class="chat_content">'+data[message].content+'<div class="cloudArrow "></div></div></div>');
//					panel.jScrollPane();
//					api.scrollTo(0,9999);
//			   }
//	    	  
//	      }
//	   });	
//};

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
	    $.getJSON("/user/dislike/",{userId:userId,page:next_page-1},function(data) {
		  if(data['result']=='success'){
			 temp.parents('.card').hide('slow');
			 card=data['card'];
			 new Card(new Person(cards.username,cards.age,cards.city,'/media/'+cards.avatar_name,cards.user_id,cards.followStatus,cards.pictureList,cards.isChat));
			 if (data['has_next']){
			 }else{
				 next_page=-1;
			 }
		 }else if(data['result']=='remove_card'){
			temp.parents('.card').hide('slow');
		 }
	 });
	 venobox();
	}
	
	var like= function(event){
	    var userId=$(this).parents('.card_panel').attr('id');
		var icon_like=$(this);
		$.getJSON("/user/update_follow/",{userId:userId},function(data) {
			  if(data.type=='error'){
				  var body = $("<p>"+data.error_message+"</p>")
		       	   $.poplayer({body:body});
				   return false;
			  }
			  if(data.type==1){
					icon_like.removeClass("icon_like_0 icon_like_1 icon_like_2 icon_like_3").addClass("icon_like_1")
					myFollow=myFollow+1
					$('#myFollow').html(myFollow)
			  }else if(data.type==2){
				  icon_like.removeClass("icon_like_0 icon_like_1 icon_like_2 icon_like_3").addClass("icon_like_2")
					follow=follow+1
					myFollow=myFollow+1
					$('#follow').html(follow)
					$('#myFollow').html(myFollow)
					
					if($('#'+userId).find('.btn_send_msg').length==0){
						var card=$('#'+userId)
						var chat_tab=$('#card').find('#chat_tab')
						card.find('#chat_tab').html(chat_tab.children());
						card.find('.btn_send_msg').on('click',sendMsg);
//						card.find(".glyphicon-comment").on('click',init_msg);
					}
				  
				  }else{
					  icon_like.following();
				     if(data.type==-1){
				    	 icon_like.removeClass("icon_like_0 icon_like_1 icon_like_2 icon_like_3").addClass("icon_like_0") 
				    	 myFollow=myFollow-1
					     $('#myFollow').html(myFollow)
				     }else{
				    	 icon_like.removeClass("icon_like_0 icon_like_1 icon_like_2 icon_like_3").addClass("icon_like_3") 
				    	 follow=follow-1
						 myFollow=myFollow-1
						 $('#follow').html(follow)
						 $('#myFollow').html(myFollow)
				     }
				     
				  };
		       
		       
		    });
		event.stopPropagation();
	};
	
	
	
	var ding = function(){
		$(this).toggleClass('ding').hasClass('ding')?$(this).attr('title','取消固定').parents('.card').removeClass('hideable'):$(this).attr('title','固定').parents('.card').addClass('hideable');
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
	
    
	function score_my(e,userId,type){
		$(e).hide().prevAll().show();
		progress = $(e).prev().prev().find('.progress-bar');
		score = $(e).prev().find('.score');
		current=$(this)
//		userId=$(this).val()
//		e.stopPropagation();    //  阻止事件冒泡
		$.ajax({
				type:'GET',
				url:'/recommend/socre_my/',
				dataType:"json",
				data:{userId:userId,type:type},
				success:function(data, textStatus){
					if(textStatus=='success'){
						if(data['result']=='success'){
							Score(data['scoreMyself'])
						}else if(data['result']=='error'){
							var body = $("<p>"+data['error_messge']+"</p>")
				       	    $.poplayer({body:body});
						}
						
					}
				},
				error:function(response){
					var body = $("<p>网络异常!</p>")
		       	    $.poplayer({body:body});
				},
		});
	}
	
	
	/*type:
		1---对比
		2--取消对比*/
	function compare(userId,type,guide){
		if(type==1){
			compare_flag=true;
			check_id=userId;
			$('#compare_button').html('取消对比')
		}else{
			compare_flag=false;
			$('#compare_button').html('与其他用户对比')
		}
		
		//引导
		if(guide){
			introBox=$('.card_row').children().not('#'+userId).first().find('.card-introBox')
			if(introBox.length){
				introBox.attr('id','compare_img')
			}
			 var tours= {
						id : "hello-hopscotch",
						steps : [{
							title : "对比信息",
							content : "点击头像就可以进行信息对比",
							target : 'compare_img',
							placement : "bottom",
							yOffset:-200,
							xOffset:100
						}]
					};
			 
			 if (!hopscotch.isActive) {
						mgr.removeAllCallouts();
						hopscotch.startTour(tours);
					}
		 }
	}
	
	//投票
	function vote(content){
		user_info=$(content).closest("#user_info")
		userId=user_info.find('#userId').val()
		score=parseInt(user_info.find('#vote_value').val().trim());
		if(isNaN(score)){
			var body = $("<p>请填写正确的格式!</p>")
       	    $.poplayer({body:body});
			return;
		}else if(score<0 || score>100){
			var body = $("<p>分数必须在1~100范围内!</p>")
       	    $.poplayer({body:body});
			return;
		}
		otherId=null;
		userList=[]
		if(compare_flag){
			$('.js-popframe').find('input[name="userId"]').each(function(){
				userList.push(parseInt(this.value));
				if(this.value!=userId){
					otherId=this.value
				}
			});
		};
		$.ajax({
			type:'POST',
			url:'/recommend/user_vote/',
			dataType:"json",
			data:{score:score,userId:userId,otherId:otherId,csrfmiddlewaretoken:getCookie('csrftoken')},
			success:function(data, textStatus){
				if(textStatus=='success'){
					if(data['result']=='success'){
						var returnData=data['data'];
						if(compare_flag){
							diagData=[returnData[userList[0]],returnData[userList[1]]];
						}else{
							diagData=[returnData[parseInt(userId)]];
						}
						$('.js-popframe').find('canvas').remove();
						$('.canvas').append('<canvas class="radar" height="290px" width="290px" style="margin-left: -38px;"></canvas>').createRadarDialog(diagData)
						$('.js-popframe').find('#score').html(data['score'])
						var body = $("<p>打分成功!</p>")
					}else if(data['result']=='error'){
						var body = $("<p>"+data['error_message']+"<p>")
					}
					$.poplayer({body:body});
				}
				
			},
			error:function(response){
				var body = $("<p>网络异常!</p>")
	       	    $.poplayer({body:body});
			},
	});
	};

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
			beforeSend:function(XMLHttpRequest){
				detail_info=false;
			},
			complete:function(XMLHttpRequest, textStatus){
				detail_info=true;
			},
			success:function(data, textStatus){
				if(data.result=='success'){
					options={
							compar:compare_flag,
							type : 'frame',
							user1 : data.user1,
					}
					if(compare_flag){
						options.user2= data.user2
						
					}
					$.poplayer(options);
					guide=data.compare_guide
					if(compare_flag){
						//取消对比
						$('#compare_button').click(function(){
							 compare(userId,2,guide)
						 })
					}else{
						$('#compare_button').click(function(){
							 compare(userId,1,guide)
						 });
						if(guide){
							//对比引导
							compare_radar_button_guide();
						}
						
					}
					$("div.dragdealer").closest('.row').find('#appearancevote').click(function(){
						vote(this);
					});
					
                    	
					$('.btn-show-score').click(function() {
						content=this;
						$.ajax({
							type:'GET',
							url:'/recommend/check_charge_for_socre_my/',
							dataType:"json",
							data:{userId:userId},
							success:function(data, textStatus){
								if(textStatus == 'success'){
					            	if( data.type=='score'){
					            		var body = $("<p>查看Ta对你的打分需消耗"+data.amount+"拼爱币。请确认？</p>")
					            		var hehe = function(){
					            			score_my(content,userId,data.type);
					            			}
					            		$.poplayer({body:body,btnFunc:hehe});
					            	}else if( data.type=='charge') {
					            		var body = $("<p>查看Ta对你的打分需消耗"+data.amount+"拼爱币。请确认？</p>")
					            		var hehe = function(){
					            			score_my(content,userId,data.type)
					            			}
					            		$.poplayer({body:body,btnFunc:hehe});
					            	}else if(data.type=='less'){
					            		var body = $("<p>请充值!</p>")
					            		 $.poplayer({body:body});
					            	} 
					            }
							},
							error:function(response){
								var body = $("<p>异常错误!</p>")
								$.poplayer({body:body});
							},
					});
						
					});
                	
				}else if(data.result=='less'){
					data.user1.data=[undefined,undefined,undefined,undefined,undefined];
					options={
							compar:compare_flag,
							type : 'frame',
							user1 : data.user1,
					}
					if(compare_flag){
						options.user2= data.user2
						
					}
					$.poplayer(options);
				}else if(data.result=='error'){
					var body = $("<p>"+data.error_message+"</p>")
		        	 $.poplayer({body:body});
				}
			},
			error:function(response){
				var body = $("<p>网络异常!</p>")
	        	 $.poplayer({body:body});
			},
	});
		}
		
	}
	this.template = $('#card').clone();

	this.template.find('.username').html(person.username).parent().attr('href','/dynamic/person/?userId='+person.userId);
	this.template.find('.user_name').html(person.username);
	this.template.find('.avatar_name').attr('src',person.headImg+'-100.jpeg')
	this.template.find('.tag').children().first().html(person.age).next().html(person.city);
	this.template.find('.head').attr('src',person.headImg+'-250.jpeg');
	this.template.find('.img-circle').attr('src',person.headImg+'-100.jpeg');
	this.template.find('.card').attr('id',person.username);
	this.template.find('.other_name').attr('title',person.username);
	this.template.find('#dynamic').attr('href','/dynamic/person/?userId='+person.userId);
	if(person.avatar_name_status=='2'){
		this.template.find('.card-introBox').append('<div class="avatar_status"><span>头像正在审核中</span></div>');
	}else if(person.avatar_name_status=='4'){
		this.template.find('.card-introBox').append('<div class="avatar_status"><span>头像审核未通过</span></div>');
	};
	//初始化详细信息href
//	this.template.find('.introBox').attr('href','/user/detailed_info/'+person.userId.toString());
    //添加用户id
	this.template.find('.card_panel').attr('id',person.userId);
	//是否关注
	var icon_like=this.template.find('.icon_like_0');
	icon_like.removeClass('icon_like_0').addClass('icon_like_'+person.isFriend);
	icon_like.attr('move-data',person.headImg+'-100.jpeg')
	if(person.isFriend=='0'||person.isFriend=='1'){
		icon_like.attr('move-to','js-follow')
	}else{
		icon_like.attr('move-to','js-follow-each')
	}
	
	//添加tab id
	var tab=this.template.find('.tab-pane');
	var nav=this.template.find('.card-nav').children();
	for (i=0;i<3;i++){
      j=i+4
	  tab[i].id='tab'+j+person.userId;
      nav.eq(i).attr('href','#tab'+j+person.userId);
	}

	for(i=0;i<person.pictureList.length;i++){
		if(i<6){
			this.template.find('.hoverbox').append('<li><a class="venobox" data-gall="gall1_'+person.userId+'" href="/media/'+person.pictureList[i].pic+'" title="'+person.pictureList[i].description+'"><img alt="demo1" src="/media/'+person.pictureList[i].smailPic+'" title="demo1"></a></li>');
		}else{
			this.template.find('.hoverbox').append('<li><a  style="display:none;" class="venobox" data-gall="gall1_'+person.userId+'" href="/media/'+person.pictureList[i].pic+'" title="'+person.pictureList[i].description+'"><img alt="demo1" src="/media/'+person.pictureList[i].smailPic+'" title="demo1"></a></li>');
		}
	}
	
		
	this.template.find('.icon_dislike,.icon_ding,.btn_send_msg,[class^="icon_like"],.glyphicon-comment,.test_match,.introBox').unbind();
	this.template.find('.username').on('click',function(event){
		event.stopPropagation();
		});
	this.template.find('.introBox').on('click',detail_info);
	this.template.find('.icon_dislike').on('click',dislike);
	
	this.template.find('.icon_ding').on('click',ding);
	
	this.template.find('i[class*="icon_like_"]').on('click',like);
	
	this.template.find(".test_match").on('click',test_match);
	this.template.find('.dafen').find('button').unbind();
	//发送私信
	if(person.isChat){
		this.template.find('.btn_send_msg').on('click',sendMsg);
//		this.template.find(".glyphicon-comment").on('click',init_msg);
	}else{
		this.template.find('#chat_tab').html('<img id="notChat" src="/static/img/no_chat.gif"/>')
	}
	if($('.card_row').length==0){
		this.template.children().hide();
		$('#search_condition').after(this.template.children());
		return;
	}
	$('.card_row').append(this.template.children());
	
	$(function(){
		$('.icon_like_0,.icon_like_3').following();
		});
	
}

function Person(username,age,city,headImg,userId,isFriend,pictureList,isChat,avatar_name_status){
	this.username = username;
	this.age = age;
	this.city = city;
	this.headImg = headImg;
	this.userId=userId;
	this.isFriend=isFriend;
	this.pictureList=pictureList;
	this.isChat=isChat;
	this.avatar_name_status=avatar_name_status;
	
}
function buy_score_for_other(context,userId){
	$.ajax({
		type:'GET',
		url:'/recommend/buy_score_for_other/',
		dataType:"json",
		data:{otherId:userId},
		success:function(data, textStatus){
			if(textStatus=='success'){
				if(data['result']=='success'){
					$(context).attr('onclick','');
					var body = $("<p>购买成功!</p>")
					if(data['type']==2){
						if($('#'+userId).find('.btn_send_msg').length==0){
							var card=$('#'+userId)
							var chat_tab=$('#card').find('#chat_tab')
							card.find('#chat_tab').html(chat_tab.children());
							card.find('.btn_send_msg').on('click',sendMsg);
//							card.find(".glyphicon-comment").on('click',init_msg);
						}
					}
				}else if(data['result']=='error'){
					var body = $("<p>"+data['error_message']+"<p>")
				}
				$.poplayer({body:body});
				
			}
			
		},
		error:function(response){
			var body = $("<p>网络异常!</p>")
       	    $.poplayer({body:body});
		},
});
}

//卡片中插入聊天
function get_card_chat(num){
	var userIdList=[];
	   var cards=$('.btn_send_msg:visible').closest('.card');
	   if(cards.length){
		   for(var i=0;i<cards.length;i++){
			   userIdList.push(cards[i].id);
		   };
		   $.getJSON('/message/get_no_read_messge_by_ids/',{num:num,userIds:userIdList.toString()},function(data){
			   for (message in data['messageList']){
			            messageBean=data['messageList'][message]
			    	    var api = pane.data('jsp');
						var chat = $('#'+messageBean.senderId).find('.jspPane')
						chat.append('<div class="chat_content_group other"><div class="chat_content">'+messageBean.content+'<div class="cloudArrow "></div></div></div>');
						pane.jScrollPane();
						api.scrollTo(0,9999);
						var jsppanel=chat.parent();
					    jsppanel.animate({scrollTop:jsppanel.height()},100)
			      }
			   set_count(data['noReadCount'])
	   });
	   };
	  
}

//对比引导按钮
function compare_radar_button_guide(){
	var compare_radar_button = {
			id : "compare_radar_button_hopscotch",
			steps : [{
				title : "与其他用户进行对比",
				content : "点击按钮可以与其他用户进行对比",
				target : "compare_button",
				placement : "bottom",
				xOffset:20
			}]
		};
		hopscotch.startTour(compare_radar_button);
}
