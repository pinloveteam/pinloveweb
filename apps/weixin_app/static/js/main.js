$(document).ready(function() {
	$('.label').click(function() {
		if ($(this).hasClass('label-success')) {
		} else {
			var selected = $(this).parent().children('.label-success');
			selected.removeClass('label-success').addClass('label-default');
			$(this).removeClass('label-default').addClass('label-success');
		}
	});
	
	$('.glyphicon-heart').click(function(){
		$(this).parent().children().removeClass('star-red');
		$(this).addClass('star-red').prevAll().addClass('star-red');
	});
	
});