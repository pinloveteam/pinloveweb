var s=["id_country","id_stateProvince","id_city"];
var opt0 = ["国家","省份、州","地级市、县"]; 
$(document).ready(function(){
	
//	     $('#id_stateProvince').bind('change',function(){
//	    	 getProvinces()
//   		 	});
//            $('#id_city').bind('change',function(){
//       		 getCities()
//       		 	});
//       	 $('#id_streetAddress').bind('change',function(){
//       		 getCounties()
//       	 	});
	 
	 $(window).load(function() {
	    	 for(i=0;i<s.length-1;i++)
	 	        document.getElementById(s[i]).onblur=new Function("change("+(i+1)+")");
	 	        change(0);
	 	       $('#id_country').bind('change',function(){
	 	    	  change(1)
	       		 	});
	       	 $('#id_stateProvince').bind('change',function(){
	       		change(2)
	       	 	});
     });
	    	 
	    
        });
 

//create the onchange        
 function Dsy()
 {
  this.Items = {};
 }
 Dsy.prototype.add = function(id,iArray)
 {
  this.Items[id] = iArray;
 }
 Dsy.prototype.Exists = function(id)
 {
  if(typeof(this.Items[id]) == "undefined") return false;
  return true;
 }

 function change(v){
  var country=$('#id_country').find("option:selected").text();
//  alert(country)
  var str="0";
  for(i=0;i<v;i++){ str+=("_"+(document.getElementById(s[i]).selectedIndex-1));};
  var ss=document.getElementById(s[v]);
  with(ss){
   length = 0;
   options[0]=new Option(opt0[v],opt0[v]);
   if(v && document.getElementById(s[v-1]).selectedIndex>0 || !v)
   {
    if(dsy.Exists(str)){
     ar = dsy.Items[str];
     for(i=0;i<ar.length;i++)
     {
    	 options[length]=new Option(ar[i],ar[i]);
    	 if(country==ar[i])
         {
//    		 alert(country+' '+ar[i])
        	 options[i+1].selected = true;
         }
     }
    	
    
     
    }
   }
  }
 }
 
//incomme
function income_choose()
{
	
	}

 