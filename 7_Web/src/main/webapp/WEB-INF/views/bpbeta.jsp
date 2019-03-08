<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<meta id="_csrf" name="_csrf" content="${_csrf.token}"/>
<meta id="_csrf_header" name="_csrf_header" content="${_csrf.headerName}"/>

<!-- Page Content -->
<input type="hidden" id="contextPathURL" value="${pageContext.request.contextPath}" />

<section class="content-section-a" id="shopping_start">
	<div class="container">
		<h2 class="beta_form_title">BlackPineapple_Beta</h2>
		<h5 class="beta_form_title">데일리룩 추천을 위한 정보를 입력해주세요</h5>
		<div class="row beta_form_row">
			<form class="row" role="form" id="joinForm" method="POST"
				action="${pageContext.request.contextPath}/data/insertCustomer" accept-charset="UTF-8"
				oninput="inputHeight.value=parseInt(h_range.value) + 100, inputWeight.value=parseInt(w_range.value) + 40">
				<div class="col-lg-5 col-md-offset-1 beta_form_div">
				<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" />
					<div class="form-group flex_form">
						<label for="inputId">아이디 : </label>
						<div id="inputIdCheck" class="alert-danger checkInput"></div>
						<input type="text" class="form-control" id="inputId" name="inputId" placeholder="아이디 (3~16 자릿수, 숫자 영문)" required>
					</div>
					<div class="form-group flex_form">
						<label for="inputPassword">패스워드 : </label>
						<div id="inputPasswordCheck" class="alert-danger checkInput"></div>
						<input type="password" class="form-control" id="inputPassword" name="inputPassword"
							placeholder="패스워드 (6~18 자릿수, 숫자 영문 특수문자 조합)" required>
					</div>
					<div class="form-group flex_form">
						<label for="inputPasswordRe"></label><input type="password" class="form-control" id="inputPasswordRe"
							name="inputPasswordRe" placeholder="패스워드 확인" required>
					</div>
					<div class="form-group flex_form">
						<label for="inputNickname">닉네임 : </label>
						<div id="inputNicknameCheck" class="alert-danger checkInput"></div>
						<input type="text" class="form-control" id="inputNickname" name="inputNickname" placeholder="닉네임" required>
					</div>
					<div class="form-group flex_form">
						<label for="inputRemark">특이사항 : </label>
						<textarea class="form-control" id="inputRemark" name="inputRemark" cols="30" rows="8"
							placeholder="특이사항을 알려주세요&#10;Ex) 알러지, 형광색 옷 기피, 셔츠만 추천해주세요 등"></textarea>
					</div>
				</div>
				<div class="col-lg-5 beta_form_div">
					<div class="form-group">
						<label for="inputShirt">평소에 입는 셔츠 사이즈를 알려주세요</label><br>
						<select class="form-control" id="inputShirt" data-rel="chosen" name="inputShirt" required="required">
							<option value="90">90(XS)</option>
							<option value="95">95(S)</option>
							<option value="100">100(M)</option>
							<option value="105">105(L)</option>
							<option value="110">110(XL)</option>
						</select>
					</div>
					<div class="form-group">
						<label for="inputPants">평소에 입는 바지 사이즈를 알려주세요</label><br>
						<select class="form-control" id="inputPants" data-rel="chosen" name="inputPants" required="required">
							<option value="25">27이하</option>
							<option value="28">28~29</option>
							<option value="30">30~31</option>
							<option value="32">32~33</option>
							<option value="34">34~35</option>
							<option value="36">36~37</option>
							<option value="38">38~39</option>
							<option value="40">40이상</option>
						</select>
					</div>
					<div class="form-group">
						<label for="inputHeight">키를 입력해주세요</label><br> 100 <input type="range" id="h_range" name="h_range" value="70">
						200 <input type="text" class="form-control" id="inputHeight" name="inputHeight" placeholder="170"
							readonly="readonly" required>
					</div>
					<div class="form-group">
						<label for="inputWeight">몸무게를 입력해주세요</label><br> 40 <input type="range" id="w_range" name="w_range"
							value="40"> 140 <input type="text" class="form-control" id="inputWeight" name="inputWeight"
							placeholder="70" readonly="readonly" required>
					</div>
				</div>
			</form>
		</div>
		<div class="modal-footer" id="joinModalFooter">
			<button type="button" class="btn btn-beta-next" id="joinSubmitBtn">
				다음페이지 <i class="fa fa-fighter-jet"></i>
			</button>
		</div>
	</div>
</section>

<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
	
	<script src="${pageContext.request.contextPath}/resources/vendor/jquery/jquery.min.js"></script>
</footer>