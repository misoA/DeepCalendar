$(document).ready(function() {
		
	var data = null;
	var token = $("meta[name='_csrf']").attr("content");
	var header = $("meta[name='_csrf_header']").attr("content");
	
	$(document).ajaxSend(function(e, xhr, options) {
        xhr.setRequestHeader(header, token);
    });
	
	$.ajax({
		url : $("#contextPathURL").val() + "/closet/get",
		type : 'GET',
		contentType : 'application/x-www-form-urlencoded; charset=UTF-8',
		dataType : 'json',
		success : function(result) {
			var data = [];
			$(result).each(function(i, j){
				$('#closet_list').append('<figure><img src = '+ j.imageUrl +'>'
					                    +'<figcaption class="figure-caption">'+j.name+'<br>#'+j.category+'<br>#'+j.weather+'<br>#'+j.type+'</figcaption></figure>');
			});
			
		}
	});
	
});

