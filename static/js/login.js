function submit(){
	$('#login').submit();
}

$(document).ready(function() {
	$.scrollUp({
		scrollName : 'scrollUp', // Element ID
		topDistance : '300', // Distance from top before showing element (px)
		topSpeed : 300, // Speed back to top (ms)
		animation : 'fade', // Fade, slide, none
		animationInSpeed : 200, // Animation in speed (ms)
		animationOutSpeed : 200, // Animation out speed (ms)
		scrollText : '', // Text for element
		activeOverlay : false // Set CSS color to display scrollUp active point, e.g '#00FFFF'
	});

	$('.btn-login,#login1,#register1').click(function() {
		$('#pinlove').slideUp('slow');
		$('#reglogin').slideDown('slow');
	});

	$(".layer-bottom").click(function() {
		$("html, body").animate({
scrollTop : $($(this).children().attr("href")).offset().top + "px"
		}, {
duration : 500,
easing : "swing"
		});
		return false;
	});
	
	$(".input-lg").keydown(function(e){
	if(e.keyCode == 13){
		submit();
		};
		});

//检查用户名
$("input[name='username']").blur(function(){
	flag=true;
	error_message=null
	error=$(this).closest('.form-group').find('#username_error')
	var username=this.value.trim();
	if (username.length==0){
		error_message='用户名不能为空!';
		flag=false;
	}else{
		re=/[\u4e00-\u9fa5a-zA-Z\xa0-\xff_][\u4e00-\u9fa50-9a-zA-Z\xa0-\xff_]{1,19}/;
		if(!re.test(username)){
			error_message='用户名格式不正确!';
    		flag=false;
		};
	}
	 if(this.id=='id_username'&&flag ){
	  $.ajax({
		type:'get',
		data:{username:username,type:'check_username'},
		url:'/account/check_register/',
		beforeSend: function(XMLHttpRequest){
         },
         success: function(data, textStatus){
	            if(textStatus == 'success'){
	            	 data=$.parseJSON(data)
	            	if(data.result=='error'){
	            		error_message=data.error_message;
	            		flag=false;
	            		error.html(error_message)
	             } 
	            	}
	    },
	     complete: function(XMLHttpRequest, textStatus){
	     },
	     error: function(response){
	    	 var body = $('<p>网络异常!</p>');
	    	 $.poplayer({body:body});
	     }
	});
	}
	  if(flag){
			  error.html('')
  	}else{
  		error.html(error_message)
  	}
  });
//验证邮箱
$('#id_email').blur(function(){
	flag=true;
	error_message=null
	error=$('#email_error')
	var email=$(this).val().trim();
	if (email.length==0){
		error_message='邮箱不能为空!';
		flag=false;
	}else{
		re=/^([a-zA-Z0-9]|[._])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
		if(!re.test(email)){
			error_message='邮箱格式错误!';
    		flag=false;
		}
	}if(flag){
	  $.ajax({
		type:'get',
		data:{email:email,type:'check_email'},
		url:'/account/check_register/',
		beforeSend: function(XMLHttpRequest){
         },
         success: function(data, textStatus){
	            if(textStatus == 'success'){
	            	 data=$.parseJSON(data)
	            	if(data.result=='error'){
	            		error_message=data.error_message;
	            		flag=false;
	            		error.html(error_message)
	             } 
	            	}
	    },
	     complete: function(XMLHttpRequest, textStatus){
	     },
	     error: function(response){
	    	 var body = $('<p>网络异常!</p>');
	    	 $.poplayer({body:body});
	     }
	});
	}
	  if(flag){
			  error.html('')
  	}else{
  		error.html(error_message)
  	}
  });

//密码错误
$('input[name^="password"]').blur(function(){
	flag=true;
	error_message=''
	error=$(this).parent().find('span[id$="error"]')
	var password=$(this).val();
	if (password==undefined ||password.length==0){
		error_message='不能为空!';
		flag=false;
	}else{
		re=/^[0-9a-zA-Z\xff_]{6,20}$/
		if(!re.test(password)){
			error_message='格式错误!';
    		flag=false;
	  }else if(this.id=='id_password2'){
		  password1=$('#id_password1').val();
		  if(password1!=password){
			  error_message='两次输入不一致，请重新输入!';
	    	  flag=false;
		  }
		  
	  }
	}
	
	if(flag){
			  error.html('')
  	}else{
  		error.html(error_message)
  	}
});

});