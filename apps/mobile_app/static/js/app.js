//查看大图
;
(function($, window, document) {
	$.fn.openPic = function(options) {
		$(this).click(function(e) {
			var picIndex = parseInt($(this).attr('name'));
			var imgEmt = $(this).parents('.pic-list').find('.js-pic-box');
			var imgArr = [];

			imgEmt.each(function() {
				imgArr.push($(this).attr('href'));
			});

			var picBox = '<div class="swiper-container pic-box"><div class="swiper-wrapper pic-wrapper">';
			for (var i = 0; i < imgArr.length; i++) {
				picBox += '<center class="swiper-slide"><img style="max-width:100%" src="' + imgArr[i] + '" /></center>';
			}
			picBox += '</div><center class="my-pagination pic-pagination"></center></div>';
			$('body').after(picBox);
			var mySwiper = $('.swiper-container').swiper({
				mode: 'horizontal',
				pagination: '.my-pagination',
				calculateHeight: true,
				initialSlide: picIndex
			});
//			if (e.state) {
//				history.replaceState({"type": "pic"}, "", "");
//			}
//			else{
//				history.pushState({"type": "pic"}, "", "?pic");
//			console.log(e.state);
//			}
//			window.onpopstate = function(e) {
//					$('.pic-box').remove();
//			}
			window.onclick = function(e) {
				if (!($(e.target).is('img'))) {
					$('.pic-box').remove();
				}
			}
		});
	}
})(jQuery, window, document, undefined);
//查看大图
//标签点击
;
(function($, window, document) {
	$.fn.label = function(options) {
		var defaults = {
			isMultiple: false,
			selectedClass: 'label-success'
		};
		var option = $.extend(defaults, options);

		$(this).find('.label').click(function(options) {
			var sC = option.selectedClass;
			if (option.isMultiple) {
				if ($(this).hasClass(sC)) {
					$(this).removeClass(sC).addClass('label-default');
				} else {
					$(this).removeClass('label-default').addClass(sC);
				}
			} else {
				$(this).parent().children().removeClass(sC).addClass('label-default');
				$(this).removeClass('label-default').addClass(sC);
			}
		});
	}
})(jQuery, window, document, undefined);
//标签点击
// QQ表情
;
(function($, window, document) {
	$.fn.qqFace = function(options) {
		var defaults = {
			id: 'facebox',
			path: 'face/',
			assign: 'content',
			tip: 'pinlove_',
			isEmojiOff: true
		};
		var option = $.extend(defaults, options);
		var assign = $('#' + option.assign);
		var id = option.id;
		var path = option.path;
		var tip = option.tip;

		if (assign.length <= 0) {
			alert('缺少表情赋值对象。');
			return false;
		}

		$(this).click(function(event) {
			var sw = $(window).width();
			var e = window.event || event;
			var strFace, labFace, subFace;
			if ($('#' + id).length <= 0) {
				//				strFace = '<div class="faceFrame row"><div id="' + id + '" style="width:' + sw * 4 + 'px;" class="qqFace">';
				strFace = '<div class="swiper-container row"><div id="' + id + '" class="swiper-wrapper">';
				for (var i = 0; i < 4; i++) {
					//					strFace += '<div class="subFace" style="width:' + sw + 'px;">';
					strFace += '<div class="swiper-slide">';
					for (var j = 1; j <= 21; j++) {
						if (i * 21 + j <= 75) {
							labFace = '{:' + tip + (i * 21 + j) + ':}';
							strFace += '<i data="cancelBubble"><img width="24px" src="' + path + (i * 21 + j) + '.png" onclick="$(\'#' + option.assign + '\').setCaret();$(\'#' + option.assign + '\').insertAtCaret(\'' + labFace + '\');" /></i>';
						}
					}
					strFace += '</div>';
				}
				strFace += '</div><center class="my-pagination"></center></div>';
			}
			$(this).parent().parent().after(strFace);
			$('#' + id).show();

			if (option.isEmojiOff) {
				e.stopPropagation();
				option.isEmojiOff = false;
				var mySwiper = $('.swiper-container').swiper({
					mode: 'horizontal',
					pagination: '.my-pagination',
					calculateHeight: true
				});
			} else {
				option.isEmojiOff = true;
			}

		});

		$(document).click(function(event) {
			var e = window.event || event;
			var target = $(e.target);
			if (!target.parents().hasClass('swiper-container')) {
				$('#' + id).parent().hide();
				$('#' + id).parent().remove();
				option.isEmojiOff = true;
			}
		});
	};

})(jQuery, window, document, undefined);

jQuery.extend({
	unselectContents: function() {
		if (window.getSelection)
			window.getSelection().removeAllRanges();
		else if (document.selection)
			document.selection.empty();
	}
});
jQuery.fn.extend({
	selectContents: function() {
		$(this).each(function(i) {
			var node = this;
			var selection, range, doc, win;
			if ((doc = node.ownerDocument) && (win = doc.defaultView) && typeof win.getSelection != 'undefined' && typeof doc.createRange != 'undefined' && (selection = window.getSelection()) && typeof selection.removeAllRanges != 'undefined') {
				range = doc.createRange();
				range.selectNode(node);
				if (i == 0) {
					selection.removeAllRanges();
				}
				selection.addRange(range);
			} else if (document.body && typeof document.body.createTextRange != 'undefined' && (range = document.body.createTextRange())) {
				range.moveToElementText(node);
				range.select();
			}
		});
	},

	setCaret: function(event) {
		if (!/msie/.test(navigator.userAgent.toLowerCase())) return;
		var initSetCaret = function() {
			var textObj = $(this).get(0);
			textObj.caretPos = document.selection.createRange().duplicate();
		};
		$(this).click(initSetCaret).select(initSetCaret).keyup(initSetCaret);
	},

	insertAtCaret: function(textFeildValue) {
		var textObj = $(this).get(0);
		if (document.all && textObj.createTextRange && textObj.caretPos) {
			var caretPos = textObj.caretPos;
			caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == '' ?
				textFeildValue + '' : textFeildValue;
		} else if (textObj.setSelectionRange) {
			var rangeStart = textObj.selectionStart;
			var rangeEnd = textObj.selectionEnd;
			var tempStr1 = textObj.value.substring(0, rangeStart);
			var tempStr2 = textObj.value.substring(rangeEnd);
			textObj.value = tempStr1 + textFeildValue + tempStr2;
			textObj.focus();
			var len = textFeildValue.length;
			textObj.setSelectionRange(rangeStart + len, rangeStart + len);
			textObj.blur();
		} else {
			textObj.value += textFeildValue;
		}
	}
});
// QQ表情插件

//js-confirm
window.Comfirm = function(title,body){
	var comfirm = $('<div class="modal fade"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><h4 class="modal-title">确认框</h4></div><div class="modal-body"><p>修改成功</p></div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">取消</button><button type="button" class="btn btn-primary" data-dismiss="modal">确认</button></div></div></div></div>');
	comfirm.find('.modal-title').html(title);
	comfirm.find('.modal-body').children().html(body);
	return comfirm;
}
