$(document).ready(function() {
		
	$('#imageUpload').on('click', function() {
		var token = $("meta[name='_csrf']").attr("content");
		var header = $("meta[name='_csrf_header']").attr("content");
		
		$(document).ajaxSend(function(e, xhr, options) {
	        xhr.setRequestHeader(header, token);
	    });
		$('#imageList').html('');
		 var form = new FormData();
		 form.append('uploadfile', $('#imageFile')[0].files[0]);
		
		$.ajax({
			url : $("#contextPathURL").val() + "/closet/imageUpload",
			type : 'POST',
			data : form,
			contentType : false,
			processData: false,
			dataType : 'json',
			success : function(result) {
				$(result.list).each(function(i, j){
					console.log(j);
					$('#imageList').append('<option data-img-class="img200" data-img-src='+ j +' value='+ j +'>');
					$("#imageList").imagepicker();
					$("#imageList").toggleClass('d-none');
				});
				
			}
		});
	});
	
//	$(document.body).on("click", '#imageList figure', function(event) {
//		$(this).toggleClass("checked_figure");
//	});
});

