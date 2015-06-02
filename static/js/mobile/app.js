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
				picBox += '<center class="swiper-slide"><img style="max-width:100%;height:auto;" src="' + imgArr[i] + '" /></center>';
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

//回复
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
//		
		
;(function($, window, document) {
	$.mobile_edit = function(options) {
		var defaults = {
				type : 'message',
				receiverId : null,
				dynamicId : null,
				init_comment : null,
				dynamicDiv:null,
			};
			var options = $.extend(defaults, options);
			edit(options.type,options.receiverId,options.dynamicId,options.init_comment,options.dynamicDiv)
		}
		function edit(type,receiverId,dynamicId,init_comment,dynamicDiv){
			if($('#edit').length>0){
				content=$('#edit');
				$('#edit').show();
			}else{
				var content=$('<div id="edit" class="edit"><div class="edit_header"><div class="row"><div class="col-xs-2"><i class="glyphicon glyphicon-chevron-left edit_close""></i></div><div class="col-xs-7">回复</div><div class="col-xs-3 edit_send">发送</div></div></div><div class="container"><form action=""  name="relpy_form" method="POST"><input id="reply_type" type="hidden" value="" name="type" id="type"><input type="hidden" name="receiverId" id="receiverId"><input type="hidden" value="" name="friendDynamicId" id="friendDynamicId"><div class="row frame"><textarea rows="6" class="form-control" id="rely_content" name="rely_content"></textarea><div class="editer-btns"><span class="emotion"></span></div></div></div></form></div>');
				content.find('.edit_send').click(function(){
					context=$(this);
					form=context.closest('.edit').find('form');
					data={csrfmiddlewaretoken:getCookie('csrftoken')}
					url="";
					receiverId=form.find('#receiverId').val();
					content=form.find('textarea').val();
					if(content.trim().length==0){
						var body=$('<p>内容不能为空!</p>')
			        	$.poplayer({body:body});
						return false;
					}
					type=form.find('#reply_type').val();
					if(type=='message'){
						url='/message/send/';
						data.receiver_id=receiverId;
						data.reply_content=content;
					}else if(type=='comment'){
						url='/dynamic/comment/';
						data.content=content;
						data.receiverId=receiverId;
						data.dynamicId=form.find('#friendDynamicId').val();
					}else{
						var body=$('<p>type参数出错!</p>')
			        	$.poplayer({body:body});
						return false;
					}
					$.ajax({
						type:'POST',
						url:url,
						dataType:"json",
						data:data,
						success:function(data, textStatus){
							if(typeof(data)!='object'){
								data=$.parseJSON(data)
							}
							if (data.result=='success'){
								content=context.closest('#edit').find('textarea').val();
								if(dynamicDiv!=null){
									data.dynamicDiv=dynamicDiv
								}
								init_comment(data)
								context.closest('#edit').find('textarea').val('');
								context.closest('.edit').hide();
						        }else if(data.result=='error'){
						        	var body=$('<p>'+data.error_message+'</p>')
						        	$.poplayer({body:body});
						        }else{
						            window.location.href='http://pinlove.com/';
						        }
							
						},
						error:function(response){
							var body = $("<p>网络异常!</p>")
				       	    $.poplayer({body:body});
						},
				});
				})
				content.find('.edit_close').click(function(){
				$('#edit').hide();
				$('#edit').find('textarea').val();
				})
				$('body').append(content)
				content.find('.emotion').qqFace({
					id: 'facebox',
					assign: 'rely_content',
					path: '/static/img/arclist/' //表情存放的路径
				});
			}
			content.find('#receiverId').val(receiverId);
			content.find('#reply_type').val(type);
			if(dynamicId!=null){
				content.find('#friendDynamicId').val(dynamicId);
			}
		}
})(jQuery, window, document, undefined);


