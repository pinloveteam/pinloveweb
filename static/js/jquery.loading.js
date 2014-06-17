;(function($, window, document) {
	var loading = $('<div><div><small>正在加载，请稍候...</small></div></div>');
	loading.css('text-align','center').find('div').css({
		'display': 'inline-block',
		'background': 'no-repeat url(./img/loading.gif)',
		'line-height': '16px',
		'padding-left': '20px'
});
	$.fn.popLoading = function() {
		this.append(loading);
	};
	$.fn.removeLoading = function() {
		loading.remove();
	};
})(jQuery, window, document, undefined);

