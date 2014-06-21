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
		} else if (options.type == 'error'){
			var dialog = options.body;
		}

		$(document.body).append(masklayer).append(dialog);

		$('.poplayer-close-btn,.masklayer,.btn-close,.compare-btn').click(function() {
			masklayer.remove();
			dialog.remove();
			$('.hopscotch-bubble').remove();
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
		var dialog = options.body;
		var ctx = dialog.find('canvas').get(0).getContext("2d");
		var datasets = {
			fillColor : "rgba(0,0,0,0)",
			strokeColor : "rgb(0,151,36)",
			pointColor : "rgb(0,151,36)",
			data:options.data
		}

		var datasets2 = {
				fillColor : "rgba(0,0,0,0)",
				strokeColor : "rgb(241,23,25)",
				pointColor : "rgb(241,23,25)",
				data:options.data2
			}

		var data = {
			labels : ["教育程度", "性格", "收入情况", "样貌", "身高"],
			datasets : [datasets,datasets2]
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

	$.poplayer = function(options) {
		var poplayer = new Poplayer(options);
	}
})(jQuery, window, document, undefined);

