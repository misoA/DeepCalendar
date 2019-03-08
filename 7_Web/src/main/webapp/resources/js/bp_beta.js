$(document).ready(function() {
	var pageContext = $("#contextPathURL").val();
	
	$('#dateRangePicker').datepicker({
		format: 'yyyy-mm-dd',
		language: "kr"
	});

	$("#joinSubmitBtn").on("click", function(event) {
		
		// 검사식
		var re_id = /^[a-z0-9_-]{3,16}$/;
		var re_nick = /^(.*).{2,16}$/;
		var re_pw = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{6,18}$/;
		var re_mail = /^([\w\.-]+)@([a-z\d\.-]+)\.([a-z\.]{2,6})$/;

		var iId = $("#inputId").val().trim();
		var iIdCheck = $("#inputIdCheck");
		iIdCheck.text("");
		var iPwd = $("#inputPassword").val().trim();
		var iPwdRe = $("#inputPasswordRe").val().trim();
		var iPwdCheck = $("#inputPasswordCheck");
		iPwdCheck.text("");
		var iNickname = $("#inputNickname").val().trim();
		var iNicknameCheck = $("#inputNicknameCheck");
		iNicknameCheck.text("");
		var iHeight = $("#inputHeight");
		var iWeight = $("#inputWeight");
		var joinForm = $("#joinForm");

		if (iId == null || iId == "") {
			iIdCheck.text("필수항목입니다");
			return;
		} else if (re_id.test(iId) != true) {
			iIdCheck.text("잘못된 형식입니다");
			return;
		} else if (iPwd == null || iPwd == "") {
			iPwdCheck.text("필수항목입니다");
			return;
		} else if (re_pw.test(iPwd) != true) {
			iPwdCheck.text("잘못된 형식입니다");
			return;
		} else if (!(iPwd == iPwdRe)) {
			iPwdCheck.text("패드워드 불일치");
			return;
		} else if (iNickname == null || iNickname == "") {
			iNicknameCheck.text("필수항목입니다");
			return;
		} else if (re_nick.test(iNickname) != true) {
			iNicknameCheck.text("닉네임의 길이가 맞지 않습니다");
			return;
		}
		var token = $("meta[name='_csrf']").attr("content");
		var header = $("meta[name='_csrf_header']").attr("content");
		
		$(document).ajaxSend(function(e, xhr, options) {
	        xhr.setRequestHeader(header, token);
	    });
		// ---------------------------------------------------------- 중복 체크
		$.ajax({
			url : $("#contextPathURL").val() + "/data/customerDuplicate",
			type : 'POST',
			data : {
				"nickname" : iNickname,
				"id" : iId
			},
			contentType : 'application/x-www-form-urlencoded; charset=UTF-8',
			dataType : 'text',
			success : function(result) {
				if (result == "both") {
					iIdCheck.text("아이디 중복");
					iNicknameCheck.text("닉네임 중복");
					return;
				} else if (result == "id") {
					iIdCheck.text("아이디 중복");
					return;
				} else if (result == "nick") {
					iNicknameCheck.text("닉네임 중복");
					return;
				} else if (result == "ok") {
					// 제출
					joinForm.submit();
				}
			}
		});
	});

	$("#styleSubmit1 figure").on("click", function(event) {
		$(this).toggleClass("checked_figure");
		var rating = $(this).find("input").eq(1).val();
		if (rating == "1") {
			$(this).find("input").eq(1).val("4");
		} else {
			$(this).find("input").eq(1).val("1");
		}
	});

	$("#noticeMailSubmitBtn").on("click", function(event) {
		var noticeMailForm = $("#noticeMailForm");
		var iEmail = $("#inputEmail");
		var iEmailCheck = $("#inputEmailCheck");
		if (iEmail.val() == null || iEmail.val() == "") {
			iEmailCheck.text("필수항목입니다");
			iEmail.focus();
		} else {
			alert("블랙파인애플 베타서비스 알림을 등록해주셔서 감사합니다")
			noticeMailForm.submit();
		}
	});

	$('#styleSubmitBtn1').on('click', function(e) {
		$('#styleSubmit1').css('display', 'none');
		$('#styleSubmit2').css('display', 'block');
		$(document).scrollTop(0);
		
	});
	
	$('#styleSubmitBtn2').on('click', function(e) {
		$('#styleSubmit2').css('display', 'none');
		$('#styleSubmit3').css('display', 'block');
		$(document).scrollTop(0);
	});
	
//	$('#styleSubmitBtn3').on('click', function(e) {
//		$('#styleSubmit3').css('display', 'none');
//		$('#styleSubmit4').css('display', 'block');
//		$(document).scrollTop(0);
//	});
	
	$('#styleSubmitBtn4').on('click', function(e) {
		$('.loading').css('display', 'block');
		$('#styleForm').submit();
	});

	$('.img-check').click(function(e) {
        $('.img-check').not(this).removeClass('check')
    		.siblings('input').prop('checked',false);
    	$(this).addClass('check')
            .siblings('input').prop('checked',true);
	});
	
	$('.img-check2').click(function(e) {
        $('.img-check2').not(this).removeClass('check')
    		.siblings('input').prop('checked',false);
    	$(this).addClass('check')
            .siblings('input').prop('checked',true);
	});
});
