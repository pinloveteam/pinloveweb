   function init() {
	var defaultMinAge=18;
	var defaultMaxAge=99
	var obj=document.getElementById('minAge')
	var op=new Option("21","21")
	op.selected = true;
	obj.add(op);
    for (i = defaultMinAge+1; i <= defaultMaxAge; i++) {
	     obj.add(new Option(""+i+"",""+i+""));
	 }
	 
	 var obj=document.getElementById('maxAge')
	 obj.add(new Option("不限","300"));
	 for (j = defaultMinAge; j <= defaultMaxAge; j++) {
	     if(j==28)
		 {
		    var op=new Option("28","28")
	        op.selected = true;
	        obj.add(op);
		 }
		 else{
		      obj.add(new Option(""+j+"",""+j+""));
		 }
	    
	 }
}
   
   
   function init1() {
	   var str = document.getElementById("maxAge");   
	   var str1 = document.getElementById("minAge");   
	   var maxAge=str.options[str.selectedIndex].value;  
	   var minAge=str1.options[str1.selectedIndex].value; 
//	   alert(maxAge+"  "+minAge)
	   if(maxAge<minAge)
	   {
			alert("年龄区间错误，请重新选择！")
			return false;
		   
	   }
	   return true;
	}
   
   function set_height()
   {
	   var defaultMinHeight=130;
		var defaultMaxHeight=226;
		var obj=document.getElementById('minHeight')
		var op=new Option("请选择","0")
		op.selected = true;
		obj.add(op);
	    for (i = defaultMinHeight+1; i <= defaultMaxHeight; i++) {
		     obj.add(new Option(""+i+"",""+i+""));
		 }
	    var obj=document.getElementById('maxHeight')
		var op=new Option("请选择","10000")
		        op.selected = true;
		        obj.add(op);
		 for (j = defaultMinHeight; j <= defaultMaxHeight; j++) {
			      obj.add(new Option(""+j+"",""+j+""));
		 }  
		 obj.add(new Option("不限","300"));
		 }
   function check_height_age() {
	   var str = document.getElementById("maxAge");   
	   var str1 = document.getElementById("minAge");   
	   var maxAge=str.options[str.selectedIndex].value;  
	   var minAge=str1.options[str1.selectedIndex].value; 
//	   alert(maxAge+"  "+minAge)
	   if(maxAge<minAge)
	   {
			alert("年龄区间错误，请重新选择！")
			return false;
		   
	   }
	   
	   var str = document.getElementById("maxHeight");   
	   var str1 = document.getElementById("minHeight");   
	   var maxHeight=str.options[str.selectedIndex].value;  
	   var minHeight=str1.options[str1.selectedIndex].value; 
//	   alert(maxHeight+"  "+minHeight)
	   if(maxHeight<minHeight)
	   {
			alert("身高区间错误，请重新选择！")
			return false;
		   
	   }
	   if((maxAge=="0"&&maxAge!="0" )||(maxAge!="0"&&maxAge=="0" )){
		   alert("请重新选择！")
			return false;
	   }
	   return true;
	}
   function add_friend(userId,count) {
//	   alert(arguments[0])
	   userId=arguments[0]
	   count=arguments[1]
	   $.getJSON("/user/addFriend/",{userId:userId},
			   function(data) {
	       $("#divmessage"+count).text(data);
	       $("#addFriend"+count).attr('disabled',true); 
	       
	    }   
	   );
   }
   
   function user_vote(userId,count) {
	   userId=arguments[0];
	   count=arguments[1];
	   score=$('#appearancescore').val()
	   $.getJSON("/recommend/user_vote/",{score:score},
			   function(data) {
	       $("#votemessage"+count).text(data);
	       if (data!='不能为空!')
	    	   {
	    	   $("#user_vote"+count).attr('disabled',true); 
	    	   }
	      
	       
	    }   
	   );
   }
      