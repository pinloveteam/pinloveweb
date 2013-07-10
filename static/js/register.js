 $(document).ready(function(){
	
            getProvinces();
            $('#id_stateProvince').bind('change',function(){
       		 getCities()
       		 	});
       	 $('#id_city').bind('change',function(){
       		 getCounties()
       	 	});
        });
        
        function getProvinces(){
            var pro = "";
            for(var i = 0 ; i < provinces.length; i++){
                pro += "<option>" + provinces[i] + "</option>";
            }
            $('#id_stateProvince').empty().append(pro);
            getCities();
        }
        function getCities(){
            var proIndex = $('#id_stateProvince').get(0).selectedIndex;
            showCities(proIndex);
            getCounties();
        }
        function showCities(proIndex){
            var cit = "";
            if(cities[proIndex] == null){
                $('#id_city').empty();
                return;
            }
            for(var i = 0 ;i < cities[proIndex].length ; i++){
                cit += "<option>" + cities[proIndex][i] + "</option>";
            }
            $('#id_city').empty().append(cit);
        }
        function getCounties(){
            var proIndex = $('#id_stateProvince').get(0).selectedIndex;
            var citIndex = $('#id_city').get(0).selectedIndex;
            showCounties(proIndex,citIndex);
        }
        function showCounties(proIndex,citIndex){
            var cou = "";
            if(counties[proIndex][citIndex] == null){
                $('#id_streetAddress').empty();
                return;
            }
            for(var i = 0 ;i < counties[proIndex][citIndex].length;i++){
                cou += "<option>" + counties[proIndex][citIndex][i] + "</option>";
            }
            $('#id_streetAddress').empty().append(cou);
        }