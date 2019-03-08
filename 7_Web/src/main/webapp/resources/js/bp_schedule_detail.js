$(document).ready(function() {

	$('#topList').imagepicker();
	$('#bottomList').imagepicker({
		initialized : function() {
			selectImage();
		}
	});

	$(document.body).on('change', '.col select', function(event) {
		selectImage();
	});

});

function selectImage() {
	// var token = $("meta[name='_csrf']").attr("content");
	// var header = $("meta[name='_csrf_header']").attr("content");
	//	
	// $(document).ajaxSend(function(e, xhr, options) {
	// xhr.setRequestHeader(header, token);
	// });
	var topImage = $('#topList').val();
	var bottomImage = $('#bottomList').val();
	var imTopCode = $('#topList option:selected').attr('data-code');
	var imBottomCode = $('#bottomList option:selected').attr('data-code');

	$.ajax({
		url : $("#contextPathURL").val() + '/schedule/getMatchRate?topImage='
				+ topImage + '&bottomImage=' + bottomImage + '&imTopCode='
				+ imTopCode + '&imBottomCode=' + imBottomCode,
		type : 'GET',
		contentType : 'application/x-www-form-urlencoded; charset=UTF-8',
		jsonpCallback : 'getMatch',
		dataType : 'text',
		success : function(result) {
			$('#matchRate').text(result);
		}
	});
}
