   function init() {
	var defaultMinAge=21;
	var defaultMaxAge=99
	var obj=document.getElementById('minAge')
	var op=new Option("21","21")
	op.selected = true;
	obj.add(op);
    for (i = defaultMinAge+1; i <= defaultMaxAge; i++) {
	     obj.add(new Option(""+i+"",""+i+""));
	 }
	 
	 var obj=document.getElementById('maxAge')
	 obj.add(new Option("不限","0"));
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
	   if(maxAge=='不限')
		   return true;
	   else{
		   if(maxAge<minAge)
			   {
			   alert("年龄区间错误，请重新选择！")
			   return false;
			   }
		   
	   }
	   return true;
	}
   
      