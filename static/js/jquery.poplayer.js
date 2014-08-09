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
			btnFunc : ''
		};
		var options = $.extend(defaults, options);

		var masklayer = $('<div class="masklayer"></div>');

		if (options.type == 'confirm') {
			var dialog = loadConfirm(options);
		} else if (options.type == 'frame') {
			var dialog = loadFrame(options);
		}

		$(document.body).append(masklayer).append(dialog);
		if(options.type == 'frame'){
			computerMove();
		}
		$('.poplayer-close-btn,.masklayer,.btn-close,.compare-btn').click(function() {
			masklayer.remove();
			dialog.remove();
		});
	}
	function is_vote(infoframe,isVote,voteScore){
		if(isVote==false){
			infoframe.find('.btn-primary').attr('disabled',true);
		    infoframe.find('.computerMove').remove();
		    infoframe.find('.score').parent().html('不能打分');
		}else{
			infoframe.find('#vote_value').val(voteScore);
			infoframe.find('.score').html(voteScore);
			infoframe.find('.progress-bar').css('width',voteScore+'%');
			infoframe.find('.computerMove').css('left',voteScore * 90 / 100 + "%")
		};
	};
	function computerMove(){
	                var $div = $("div.computerMove");
	                if($div.length==0){
	                	return;
	                }
					var progressWidth = $div.parents('.progress').css('width').split('p')[0];
					/* 绑定鼠标左键按住事件 */
					$div.bind("mousedown", function(event) {
						var moveDiv = $(this);

						var progress = moveDiv.parent();

						var score = moveDiv.parents('.row').find('.score');
						/* 获取需要拖动节点的坐标 */
						var offset_x = moveDiv[0].offsetLeft;
						//x坐标

						/* 获取当前鼠标的坐标 */
						var mouse_x = event.pageX;

						/* 绑定拖动事件 */
						/* 由于拖动时，可能鼠标会移出元素，所以应该使用全局（document）元素 */
						$(document).bind("mousemove", function(ev) {
							/* 计算鼠标移动了的位置 */
							var _x = ev.pageX - mouse_x;

							/* 设置移动后的元素坐标 */
							var now_x = Math.round((offset_x + _x) / progressWidth * 100);

							/* 改变目标元素的位置 */
							if (now_x >= 0 && (_x < -5 || now_x <= 100)) {
								moveDiv.css({
									left : now_x * 90 / 100 + "%"
								});
								progress.css({
									width : now_x + "%"
								});
								score.html(now_x);
								$('#vote_value').val(now_x);
								
							}
						});
					});

					$(document).bind("mouseup", function() {
						$(this).unbind("mousemove");
					});
	}
	function loadConfirm(options) {
		var dialog = $('<div class="poplayer"><div class="poplayer-confirm"><div class="poplayer-confirm-head"><span class="poplayer-confirm-head-text text-white"></span><span class="poplayer-close-btn text-white">X</span></div><div class="poplayer-confirm-body"></div><div class="poplayer-confirm-bottom"><button class="btn btn-info btn-close"></button></div></div></div>');
		dialog.find('.poplayer-confirm-head-text').html(options.head);
		dialog.find('.poplayer-confirm-body').html(options.body);
		dialog.find('button').html(options.btnText).bind('click', options.btnFunc);
		return dialog;
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
		var i1 = $('<div class="col-xs-4" style="padding-left: 0;"><img id="head" width="75px" src=""/></div><div class="col-xs-8" style="padding-right: 0;"><input type="hidden" id="userId" value=""><div class="name"><span id="name"></span><div class="info"><span id="age"></span>岁&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span id="city"></span></div></div><div class="score-other"><div class="col-xs-8" style="padding: 0; display: none;"><div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100" style="width: 0%"></div></div></div><div class="col-xs-4" style="padding-right: 0; display: none;"><span class="score">0</span>分</div><button class="btn btn-xs btn-info btn-show-score">查看TA对你的打分</button></div></div></div>');
		i1.find('#head').attr('src', user.head);
		i1.find('#name').html(user.name);
		i1.find('#age').html(user.age);
		i1.find('#city').html(user.city);
		i1.find('#userId').val(user.userId);
		

		var i2 = $('<div class="row"><hr /><p class="title">性格标签</p><div class="tags"></div></div>');
		user.tag.forEach(function(e) {
			i2.find('.tags').append('<span class="tag">' + e + '</span>');
		});

		var i3 = $('<div class="row"><hr /><p class="title">详细信息</p><table class="table"><tbody><tr><td>身高：<span id="height"></span></td><td>学历：<span id="education"></span></td></tr><tr><td>年龄：<span id="age"></span></td><td>收入：<span id="income"></span></td></tr><tr><td>行业：<span id="trade"></span></td><td>星座：<span id="constellation"></span></td></tr></tbody></table></div>');
		i3.find('#height').html(user.height);
		i3.find('#education').html(user.education);
		i3.find('#age').html(user.age);
		i3.find('#trade').html(user.trade);
		i3.find('#income').html(user.income);
		i3.find('#constellation').html(user.constellation);

		var i4 = $('<div class="row"><hr /><p class="title">为TA打分</p><div class="col-xs-6" style="padding: 0;"><div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100" style="width: 0%"><div class="computerMove"></div></div></div></div><div class="col-xs-3" style="padding-right: 0;"><span class="score">0</span>分<input id="vote_value" type="hidden" value=""></div><div class="col-xs-3"><button id="appearancevote" class="btn btn-xs btn-primary">确认</button></div></div>');
		//判断能不能投票
		is_vote(i4,user.isVote,user.voteScore);
		infoframe.append(i1).append(i2).append(i3).append(i4);
		
		return infoframe;
	}

	function loadRadarFrame(options) {
		var dataArry = new Array();
		var radarframe = $('<div class="col-xs-3" style="background-color: #100B31; height: 503px; padding: 25px;"></div>');
		radarframe.addClass('radius');

		var r1 = $('<div class="row"><div class="col-xs-6"><img id="head" width="55px" src=""/></div><div class="col-xs-6" style="padding-top: 23px;padding-left: 0;"><span id="score" class="score-big" style="color: red;"></span><span class="text">分</span></div></div><div class="row"><div class="col-xs-12"><button id="compare_button" class="btn btn-xs btn-danger compare-btn">与其他用户对比</button></div></div>');
		r1.find('#head').attr('src', options.user1.head);
		r1.find('#score').html(options.user1.score);
		radarframe.append(r1);

//		var r3 = $('<div class="row"><div class="col-xs-12"><button class="btn btn-xs btn-danger">与其他用户对比</button></div></div>')
		var r2 = $('<div class="row"><canvas class="radar" height="290px" width="290px" style="margin-left: -38px;"></canvas></div>');
		radarframe.append(r2);
		var ctx = radarframe.find('canvas').get(0).getContext("2d");
		var datasets = {
			fillColor : "rgba(0,0,0,0)",
			strokeColor : "rgb(0,151,36)",
			pointColor : "rgb(0,151,36)",
			data : options.user1.data
		}

		dataArry.push(datasets);
		if (options.compar == true) {
			radarframe.removeClass('radius');
			r1.find('.compare-btn').html('取消对比');
			var r3 = $('<div class="row"><div class="col-xs-6"><img id="head" width="55px" src=""/></div><div class="col-xs-6" style="padding-top: 23px;padding-left: 0;"><span id="score" class="score-big" style="color: green;"></span><span class="text">分</span></div></div>');
			r3.find('#head').attr('src', options.user2.head);
			r3.find('#score').html(options.user2.score);
			radarframe.append(r3);
			var datasets2 = {
				fillColor : "rgba(0,0,0,0)",
				strokeColor : "rgb(241,23,25)",
				pointColor : "rgb(241,23,25)",
				data : options.user2.data
			}
			dataArry.push(datasets2);
		}
		var data = {
			labels : ["教育程度", "性格", "收入情况", "样貌", "身高"],
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

		return radarframe;
	}


	$.poplayer = function(options) {
		var poplayer = new Poplayer(options);
	}
})(jQuery, window, document, undefined);

