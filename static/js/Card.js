var labels = ["教育程度","性格","收入情况","样貌","身高"]
var datasets_self = {fillColor : "rgba(0,0,0,0)",strokeColor : "rgb(0,151,36)",pointColor : "rgb(0,151,36)"}
var datasets_other = {fillColor : "rgba(0,0,0,0)",strokeColor : "rgb(241,23,25)",pointColor : "rgb(241,23,25)"}
var comparable = false;
var name_self = '';
var name_other = '';
var dataArray = {};
window.Card = function(person){
	
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
					icon_like.removeClass("icon_like_0").addClass("icon_like_1")
					myFollow=myFollow+1
					$('#myFollow').html(myFollow)

			  }else if(data['type']==2){
				  icon_like.removeClass("icon_like_0").addClass("icon_like_2")
					follow=follow+1
					myFollow=myFollow+1
					$('#follow').html(follow)
					$('#myFollow').html(myFollow)
				  }else{
					  icon_like.removeClass("icon_like_1").removeClass("icon_like_2").addClass("icon_like_0") 
				     if(data['type']==-1){
				    	 myFollow=myFollow-1
					     $('#myFollow').html(myFollow)
				     }else{
				    	 follow=follow-1
						 myFollow=myFollow-1
						 $('#follow').html(follow)
						 $('#myFollow').html(myFollow)
				     }
				     
				  };
		       alert(data['content']);
		       
		       
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
	
	var showRadar = function(){
		if(this.isRadarShow){
		$(this).children().not('.name').hide('fast');
			this.isRadarShow = false;
		}
		else{
			$(this).find("canvas").show('fast');
			var ctx = $(this).find("canvas").get(0).getContext("2d");
			$(this).find(".compare").show('fast');
			var name = $(this).attr('title');
			datasets_self.data = dataArray[name];
			var data = {labels : labels, datasets : [datasets_self]};
			var myNewChart = new Chart(ctx).Radar(data,{scaleOverride:true,scaleSteps:4,scaleStepWidth:25,scaleStartValue:0,scaleLineColor : "rgba(0,0,0,.5)",angleLineColor : "rgba(0,0,0,.5)"});
			this.isRadarShow = true;
		}
	}
	
	var compareRadar = function(){
		if(this.isRadarShow){
			$(this).children().not('.name').hide('fast');
			this.isRadarShow = false;
		}
		else{
			$(this).find("canvas").show('fast');
			var ctx = $(this).find("canvas").get(0).getContext("2d");
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
		}
	}
	
	var compare = function(){
		$(this).parents('.card').addClass('chosen');
		$(this).hide().find('.compare_cancle').show('fast');
		name_self = $(this).parent().attr('title');
		$('#compare_tip').show('slow',function(){
			$(this).delay(2000).hide('slow');
		});
		comparable = true;
		
		$('.other_name').unbind();
		$('.other_name').on('click',compareRadar);
	}
	
	var compare_cancle = function(){
		$('.chosen').removeClass('chosen');
		$(this).hide().find('.compare').show('fast');
		comparable = false;
		name_other = '';
		name_self = '';
		
		$('.other_name').unbind();
		$('.other_name').on('click',showRadar);
	}
	
	this.template = $('#card').clone();

	this.template.find('.username').html(person.username);
	this.template.find('.tag').children().first().html(person.age).next().html(person.city);
	this.template.find('.head').children().attr('src',person.headImg+'-110.jpeg');
	this.template.find('.min_head').children().attr('src',person.headImg+'-60.jpeg');
	this.template.find('.card').attr('id',person.username);
	this.template.find('.other_name').attr('title',person.username);
	//初始化详细信息href
	this.template.find('.introBox').attr('href','/user/detailed_info/'+person.userId.toString());
	 //初始化数组
     dataArray[person.username]= [person.heighScore,person.incomeScore,person.edcationScore,person.appearanceScore,person.characterScore,];
    //添加用户id
	this.template.find('.card_panel').attr('id',person.userId);
	//是否关注
	var icon_like=this.template.find('.tool_bar :nth-child(2) ').children();
	icon_like.removeClass().addClass('icon_like_'+person.isFriend);
	//添加tab id
	var tab=this.template.find('.tab-pane');
	var nav=this.template.find('.card-nav').children().children();
	for (i=0;i<3;i++){
      j=i+4
	  tab[i].id='tab'+j+person.userId;
	  nav[i].href='#tab'+j+person.userId;
	}

	
	for (i=0;i<4;i++){
		this.template.find('.hoverbox').append('<li><a class="venobox" data-gall="gall1" href="/static/img/img2.jpg" title="ss"><img alt="demo1" src="/static/img/img2.jpg" title="demo1"></a></li>');
	}
		
	$('.card_row').append(this.template.html());
	
	$('.icon_dislike,.icon_ding,.btn_send_msg,.other_name,.compare,.compare_cancle,[class^="icon_like"],.icon_msg').unbind();
	
	$('.icon_dislike').on('click',dislike);
	
	$('.icon_ding').on('click',ding);
	
	$('.btn_send_msg').on('click',sendMsg);
	
	$('.other_name').on('click',showRadar);
	
	$('.compare').on('click',compare);
	
	$('.compare_cancle').on('click',compare_cancle);
	
	$("[class^='icon_like']").on('click',like);
	
	$(".icon_msg").on('click',init_msg);
}

function Person(username,age,city,headImg,userId,isFriend){
	this.username = username;
	this.age = age;
	this.city = city;
	this.headImg = headImg;
	this.userId=userId;
	this.isFriend=isFriend;
	
}