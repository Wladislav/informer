(function($) {
    "use strict";
		  $("#defualt" ).on('click',function(){
			  $("#color" ).attr("href", "/static/css/colors/defualt.css");
			  return false;
		  });
		  
		 
		  $("#red" ).on('click',function(){
			  $("#color" ).attr("href", "/static/css/colors/red.css");
			  return false;
		  });
		  
		   $("#green" ).on('click',function(){
			  $("#color" ).attr("href", "/static/css/colors/green.css");
			  return false;
		  });
		  
		  $("#blue" ).on('click',function(){
			  $("#color" ).attr("href", "/static/css/colors/blue.css");
			  return false;
		  });
		  
		
		   $("#sea-green" ).on('click',function(){
			  $("#color" ).attr("href", "/static/css/colors/sea-green.css");
			  return false;
		  });
		  
	
		  // picker buttton
		  $(".picker_close").click(function(){
			  	$("#choose_color").toggleClass("position");
			  
		   });
		  
})(jQuery);