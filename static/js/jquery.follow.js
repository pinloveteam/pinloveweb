;(function($, window, document) {
	$.extend($.fn, {
		following : function(options) {
			var self = this;
			$follow = $('.'+$(self).attr('move-to'));
			var F = {
				init : function() {
					$(self).data('click', true).on('click', this.addfollowing);
				},
				addfollowing : function(e) {
					e.stopPropagation();
					var $target = $(e.target), 
					$img = $target.attr('move-data');
					id = $target.attr('id'), 
					dis = $target.data('click'),
					x = $target.offset().left + 30, 
					y = $target.offset().top + 10, 
					X = $follow.offset().left + $follow.width() / 2 - $target.width() / 2 + 10, 
					Y = $follow.offset().top;
					if (dis) {
						if ($('#floatOrder').length <= 0) {
							floatOrder = $('<div id="floatOrder"><img width="50" height="50" /></div');
							floatOrder.find('img').attr('src',$img);
							floatOrder.css({
								'width' : '50px',
								'height' : '50px',
								'padding' : '2px',
								'background' : '#fff',
								'border' : 'solid 5px #e54144',
								'overflow' : 'hidden',
								'position' : 'absolute',
								'z-index' : '890'
							});
							$('body').append(floatOrder);
						};
						var $obj = $('#floatOrder');
						if (!$obj.is(':animated')) {
							$obj.css({
								'left' : x,
								'top' : y
							}).animate({
								'left' : X,
								'top' : Y - 80
							}, 500, function() {
								$obj.stop(false, false).animate({
									'top' : Y - 20,
									'opacity' : 0
								}, 500, function() {
									$obj.fadeOut(300, function() {
										$obj.remove();
										$target.data('click', false);
									});
								});
							});
						};
					};
				}
			};
			F.init();
		}
	});
})(jQuery, window, document, undefined);

