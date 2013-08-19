
$(document).ready(function(){
	    
        });
 
function check_login()
{
	var is_gener_choose=$('input:radio[name="gender"]:checked').val();
//	alert(is_gener_choose)
	if(is_gener_choose==null) 
		{
		    alert("请选择性别！")
		    return false;
		}
	return true;
	}


 