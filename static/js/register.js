var area=["id_country","id_stateProvince","id_city"];
var opt0 = ["请选择","请选择","请选择"]; 
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
	    	 for(i=0;i<area.length-1;i++)
	 	        document.getElementById(area[i]).onblur=new Function("change("+(i+1)+")");
	    	    for(var i=0;i<3;i++){
	    	    	change(i);
	    	    }
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
  var country=$('#'+area[v]).find("option:selected").text();
//  alert(country)
  var str="0";
  for(i=0;i<v;i++){ str+=("_"+(document.getElementById(area[i]).selectedIndex-1));};
  var ss=document.getElementById(area[v]);
  with(ss){
   length = 0;
   options[0]=new Option(opt0[v],opt0[v]);
   if(v && document.getElementById(area[v-1]).selectedIndex>0 || !v)
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

 