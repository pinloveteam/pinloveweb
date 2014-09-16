load_next_page=true;
var next_page=0;
var totalheight = 0; 
(function($){
			$.fn.extend({
			insertAtCaret: function(myValue){
			var $t=$(this)[0];
			if (document.selection) {
			this.focus();
			sel = document.selection.createRange();
			sel.text = myValue;
			this.focus();
			}
			else
			if ($t.selectionStart || $t.selectionStart == '0') {
			var startPos = $t.selectionStart;
			var endPos = $t.selectionEnd;
			var scrollTop = $t.scrollTop;
			$t.value = $t.value.substring(0, startPos) + myValue + $t.value.substring(endPos, $t.value.length);
			this.focus();
			$t.selectionStart = startPos + myValue.length;
			$t.selectionEnd = startPos + myValue.length;
			$t.scrollTop = scrollTop;
			}
			else {
			this.value += myValue;
			this.focus();
			}
			}
			})
			})(jQuery);


function stop_load_next_page(){
	load_next_page=false;
};
function get_load_next_page(){
	return load_next_page
}
//滚动加载
//no_load不加载   ,success成功
function loadData(no_load,success)
{ 
    totalheight = parseFloat($(window).height()) + parseFloat($(window).scrollTop()); 

    if ($(document).height() <= totalheight) 
	{ 
		//加载数据
		if(next_page==-1){
			return no_load()
		}
		if(load_next_page==true){
		
		 $.ajax({
	         type: 'GET',
	         url:window.location.pathname,
	         data:{page:next_page},
	         beforeSend: function(XMLHttpRequest){
	        	 load_next_page=false;
	         },
	         success: function(data, textStatus){
	        	 success(data);
	         },
	         complete: function(XMLHttpRequest, textStatus){
	        	 load_next_page=true;
	         },
	         error: function(response){
	             alert('网络异常!')
	         }
	     });
		 
		};
    } 
} 