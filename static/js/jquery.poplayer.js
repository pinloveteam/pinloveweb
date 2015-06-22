//调用方式$.poplayer(options);
//options={
//	head : '确认',
//	body : 'message',
//	btnText : '确定',
//	btnFunc : this.closeDialog
//}

//OR

//options={
//	type : 'frame',
//	body : 'message',
//}
;(function($, window, document) {
	var Poplayer = function(options) {
		var defaults = {
			type : 'confirm',
			head : '确认',
			body : 'message',
			btnText : '确定',
			btnFunc : '',
			singleBtn :true
		};
		var options = $.extend(defaults, options);

		if (options.type == 'confirm') {
			var dialog = loadConfirm(options);
		} else if (options.type == 'frame') {
			var masklayer = $('<div class="masklayer"></div><div class="msk-close">X</div>');
			masklayer.remove();
			var dialog = loadFrame(options);
		}

		$(document.body).append(masklayer).append(dialog);
		if (options.type == 'frame') {
			var isVoteList=new Array();
			isVoteList.push(options.user1.isVote);
			var voteScoreList=new Array();
			voteScoreList.push(options.user1.voteScore);
			if(options.compar==true){
				isVoteList.push(options.user2.isVote);
				voteScoreList.push(options.user2.voteScore);
			}
			is_vote(dialog,isVoteList,voteScoreList);
			//雷达图显示网站所需显示提示
			if(options.user1.error_message!=undefined){
			 recommendStatus=options.user1.error_message;
			 txt='<span class="tip">如需查看对方的雷达图和打分，必须完善你的</span>'
			 for(var v in recommendStatus){
				txt= txt+'<span class="text-red"><a href="'+recommendStatus[v].href+'">'+recommendStatus[v].info+'</a>  </span>'
			 }
	         recommend_status_tip(txt);
			}
		}
		$('.poplayer-close-btn,.masklayer,.btn-close,.compare-btn,.js-popframe,.msk-close').click(function() {
			masklayer.remove();
			dialog.remove();
			$('.hopscotch-nav-button').click();
		});
		
	}
	function is_vote(infoframe,isVote,voteScore){
		var dragdealerList=$('.dragdealer');
		dragdealerList.each(function(index){
			if(isVote[index]==false){
				$(this).parents('.row').find('.btn-primary').attr('disabled',true);
				$(this).parents('.row').find('.score').html('不能打分');
			    new Dragdealer(this.id, {
					  animationCallback: function(x, y) {
					  },
					  disabled:true
					});
			    $(this).attr('title','对方相貌没有上传或审核通过')
			}else{
				$(this).parents('.row').find('.score').html(voteScore[index]);
				var context=this.id;
			    new Dragdealer(this.id, {
					  animationCallback: function(x, y) {
						  row=$('#'+context).parents('.row');
					    row.find('.score').text(Math.round(x * 100)+'分');
					    row.find('#vote_value').val(Math.round(x * 100))
					  },
					  x:voteScore[index]/100
					});
			    $(this).attr('title','拖动打分')
			};
			
		});
	};
	

	function loadConfirm(options) {
		var comfirm = $('<div class="modal fade"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button><h4 class="modal-title">确认框</h4></div><div class="modal-body"><p>修改成功</p></div><div class="modal-footer"><button id="confirm" type="button" class="btn btn-primary" data-dismiss="modal">确认</button></div></div></div></div>');
		comfirm.find('.modal-title').html(options.head);
		comfirm.find('.modal-body').children().html(options.body);
		comfirm.modal('show');
		if(options.btnFunc!=undefined){
			comfirm.find('#confirm').click(options.btnFunc);
		}
		comfirm.find('#confirm').html(options.btnText);
		
		return comfirm;
	}

	function loadFrame(options) {
		var frame = $('<div class="container js-popframe"></div>');
		var infoframe = loadInfoFrame(options.user1).addClass('left');
		var radarframe = loadRadarFrame(options);
		frame.append(infoframe).append(radarframe);
		if(options.compar==true){
			frame.append(loadInfoFrame(options.user2).addClass('right'));
		}
		return frame;
	}

	function loadInfoFrame(user) {
		var infoframe = $('<div id="user_info"  class="col-xs-4"></div>');
		infoframe.click(function(){
			return false;
		});
		var i1 = $('<div class="row"><div class="col-xs-4" style="padding-left: 0;"><img id="head" width="75px" src=""/></div><div class="col-xs-8" style="padding-right: 0;height: 80px;"><input type="hidden" name="userId" id="userId" value=""><div class="name"><span id="name"></span><div class="info"><span id="age"></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span id="city"></span></div></div><div class="score-other"><div style="position: relative; top: 10px;"><p>TA对你的打分</p></div><div class="col-xs-8" style="padding: 0; display: none;"><div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100" style="width: 0%"></div></div></div><div class="col-xs-4" style="padding-right: 0; padding-left:6px; display: none;"><span class="score">0</span>分</div><button class="btn btn-xs btn-info btn-show-score">查看TA对你的打分</button></div></div></div></div>');
		i1.find('#head').attr('src', user.head);
		i1.find('#name').html(user.name);
		i1.find('#age').html(user.age);
		i1.find('#city').html(user.city);
		i1.find('#userId').val(user.userId);
		if(user.scoreMy>=0){
			var show_score=i1.find('.btn-show-score');
			show_score.hide().prevAll().show();
			progress = show_score.prev().prev().find('.progress-bar');
			score = show_score.prev().find('.score');
			progress.css({
				width : user.scoreMy + "%"
			});
			score.html(user.scoreMy);
		}
		

		var i2 = $('<div class="row"><hr /><p class="title">性格标签</p><div class="tags"></div></div>');
		user.tag.forEach(function(e) {
			i2.find('.tags').append('<span class="tag">' + e + '</span>');
		});

		var i3 = $('<div class="row"><p class="title">详细信息</p><table class="table"><tbody><tr><td>身高：<span id="height"></span></td><td>学历：<span id="education"></span></td></tr><tr><td>年龄：<span id="age"></span></td><td>收入：<span id="income"></span></td></tr><tr><td>行业：<span id="trade"></span></td><td>星座：<span id="constellation"></span></td></tr></tbody></table></div>');
		i3.find('#height').html(user.height);
		i3.find('#education').html(user.education);
		i3.find('#age').html(user.age);
		i3.find('#trade').html(user.trade);
		i3.find('#income').html(user.income);
		i3.find('#constellation').html(user.constellation);

		var i4 = $('<div class="row"><hr /><p class="title">为TA相貌打分</p><div class="col-xs-6" style="padding: 0;"><div class="dragdealer" id="slider-'+user.userId+'"><div class="handle red-bar" style="perspective: 1000px; backface-visibility: hidden; transform: translateX(144px);"></div></div></div><div class="col-xs-3" style="padding-right: 0;"><span class="score" style="font-size:14px;">0</span><input id="vote_value" type="hidden" value=""></div><div class="col-xs-3"><button id="appearancevote" class="btn btn-xs btn-primary">确认</button></div></div>');
		infoframe.append(i1).append(i2).append(i3).append(i4);
		
		return infoframe;
	}
	//判断雷达图每个属性是否填写完整
	function is_info_finish(r_div,user){
		var INFO={
				'score_full':'该用户信息没有填写完整',
				'score_tooltip':'如果雷达图中的某项分数为0，则该用户可能没有完整填写该项信息。',
		};
		var userList=[user.education,user.tag.length==0?'未填':0,user.income,user.isVote==false?'未填':0,user.height]
		for(var key in user.data){
			if(user.data[key]==0 && userList[key]=='未填'){
				r_div.find('.info_warn').append('<span style="text-align: center;color: red;">'+INFO['score_full']+'</span>&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-question-sign" style="color:#e7e7e7;" data-toggle="popover" data-placement="left" data-content="'+INFO['score_tooltip']+'" ></span>');
				r_div.find('[data-toggle="popover"]').popover({
				    trigger: 'hover',
				    'placement': 'top',
				    template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>'
				});
				break;
			}
		};
		
	}

	function loadRadarFrame(options) {
		
		var score_warn_content=''
		var dataArry = new Array();
		var radarframe = $('<div class="col-xs-3" style="background-color: #100B31; padding: 25px;"></div>');
		radarframe.addClass('radius');
		radarframe.click(function(){
			return false;
		});
		var r1 = $('<div class="row"><div class="col-xs-6"><img id="head" width="55px" src=""/></div><div class="col-xs-6" style="padding-top: 23px; padding-left: 0px; height: 60px;top: -20px;"><div><span style="color: white;">TA的得分</span></div><div><span id="score" class="score-big" style="color: red;">0</span><span class="text">分</span></div></div></div><div class="row"><div class="col-xs-12"><button id="compare_button" class="btn btn-xs btn-danger compare-btn">与其他用户对比</button></div><div class="col-xs-12 info_warn" ></div></div>');
		r1.find('#head').attr('src', options.user1.head);
		r1.find('#score').html(options.user1.score);
		if(options.user1.error_message!=undefined){
			r1.find('#score').next().remove();
			r1.find('#score').remove();
			var info = r1.find('#compare_button').parent();
			r1.find('#compare_button').remove();
			
		}else{
			is_info_finish(r1,options.user1);
		}
		
		radarframe.append(r1);

//		var r3 = $('<div class="row"><div class="col-xs-12"><button class="btn btn-xs btn-danger">与其他用户对比</button></div></div>')
		var r2 = $('<div id="radar_canvus" class="row canvas"><canvas class="radar" height="290px" width="290px" style="margin-left: -38px;"></canvas></div>');
		radarframe.append(r2);
		dataArry.push(options.user1.data);
		if (options.compar == true) {
			radarframe.removeClass('radius');
			r1.find('.compare-btn').html('取消对比');
			var r3 = $('<div class="row"><div class="col-xs-6"><img id="head" width="55px" src=""/></div><div class="col-xs-6" style="padding-top: 23px; padding-left: 0px; height: 60px;top: -20px;"><div><span style="color: white;">TA的得分</span></div><span id="score" class="score-big" style="color: green;"></span><span class="text">分</span></div><div class="col-xs-12 info_warn"><p style="text-align: center;color: red;"></p></div></div>');
			r3.find('#head').attr('src', options.user2.head);
			r3.find('#score').html(options.user2.score);
			
			is_info_finish(r3,options.user2);
			radarframe.append(r3);
			dataArry.push(options.user2.data);
		}
        radarframe.createRadarDialog(dataArry)
		return radarframe;
	}
	
	//创建雷达图
	$.fn.createRadarDialog = function(dataList) {
	    dataArry=new Array()
		var strokeColorList=["rgb(241,23,25)","rgb(0,151,36)"];
		var pointColorList=["rgb(241,23,25)","rgb(0,151,36)"];
		for(var i=0 ;i<dataList.length;i++){
		var datasets = {
				fillColor : "rgba(0,0,0,0)",
				strokeColor : strokeColorList[i],
				pointColor : pointColorList[i],
				data : dataList[i]
			};
		dataArry.push(datasets);
		};
	   
		var ctx = $(this).find('canvas').get(0).getContext("2d");
		var data = {
			labels : ["教育程度",  "收入","性格", "身高", "相貌"],
			datasets : dataArry
		};
		var myNewChart = new Chart(ctx).Radar(data, {
			scaleOverride : true,
			scaleSteps : 4,
			scaleStepWidth : 25,
			scaleStartValue : 0,
			scaleLineColor : "rgba(255,255,255,.5)",
			//				scaleShowLabels : true,
			pointLabelFontColor : '#fff',
			angleLineColor : "rgba(255,255,255,.5)"
		});
	};
	


	$.poplayer = function(options) {
		var poplayer = new Poplayer(options);
	}
})(jQuery, window, document, undefined);

function Score(s) {
	num = s;
	clearInterval(Time);
	Time = setInterval(Start, 3);
	progress.css({
		width : num + "%"
	});
}

function Start() {
	if (i <= num) {
		score.html(i);
		i++;
	} else {
		clearInterval(Time);
		i = 0;
	}
} 

//显示完整雷达图需要填写信息提示
function recommend_status_tip(data){
	var recommend_status_tip = {
			id : "recommend_status_tip",
			steps : [{
				title : "显示完整雷达图",
				content : data,
				target : "radar_canvus",
				placement : "bottom",
				xOffset:100,
				yOffset:-50,
			},]
		};
		hopscotch.startTour(recommend_status_tip);
}