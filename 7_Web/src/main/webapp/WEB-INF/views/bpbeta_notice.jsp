<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!-- Navigation -->
<nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
	<div class="container">
		<a class="navbar-brand" href="${pageContext.request.contextPath}/bpbeta/notice"><img class="nav-logo" src="${pageContext.request.contextPath}/resources/img/logo/PNG/BLACKPINEAPPLE_MAIN_05.png"
					alt="LOGO"> BlackPineapple_Beta</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive"
			aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarResponsive">
			<ul class="navbar-nav ml-auto">
				<li class="nav-item">
					<a class="nav-link" href="${pageContext.request.contextPath}/bpinfo/">BlackPineapple 서비스 소개</a>
				</li>

			</ul>
		</div>
	</div>
</nav>

<!-- Page Content -->
<input type="hidden" id="contextPathURL" value="${pageContext.request.contextPath}" />
<section class="content-section-b beta_top" id="content-section-b">
	<div class="container">
		<div class="row beta_top_row">
			<div class="clearfix"></div>
			<h2 class="section-heading">블랙파인애플의 추천 데일리룩</h2>
			<p class="lead beta_top_lead">
				블랙파인애플은 <b>인공지능 패션 추천 알고리즘</b>으로 <br> 귀찮은 쇼핑을 쉽고 빠르게 해결해드립니다. <br> <b>블랙파인애플_Beta</b>를 통해 먼저 체험해보세요
			</p>
			<a class="btn btn-beta" href="#shopping_notice">Beta 서비스 알림 받기</a>
		</div>
	</div>
</section>

<section class="content-section-a" id="shopping_notice">
	<div class="container">
		<h2 class="beta_form_title">BlackPineapple_Beta</h2>
		<h5 class="beta_form_title">Beta 서비스가 시작되면 메일로 알려드립니다</h5>
		<div class="row beta_form_row">
			<div class="col-lg-8 beta_form_div">
				<form role="form" id="noticeMailForm" method="POST" action="${pageContext.request.contextPath}/data/noticeMailSend"
					accept-charset="UTF-8">
					<div class="form-group">
						<label for="inputEmail">이메일</label>
						<div id="inputEmailCheck" class="alert-danger checkInput"></div>
						<input type="text" class="form-control" id="inputEmail" name="inputEmail" placeholder="알림받을 메일 주소를 적어주세요">
					</div>
					<div class="form-group">
						<label for="inputContents">Contact</label>
						<textarea cols="10" rows="10" class="form-control" id="inputContents" name="inputContents" placeholder="블랙파인애플 팀에게 하고 싶은 이야기를 적어주세요" ></textarea>
						
					</div>
				</form>
			</div>
		</div>
		<div class="modal-footer" id="joinModalFooter">
			<button type="button" class="btn btn-beta-next" id="noticeMailSubmitBtn">
				알림 받기 <i class="fa fa-fighter-jet"></i>
			</button>
		</div>
	</div>
</section>

<aside class="banner beta_banner" id="snsbanner">
	<div class="container">
		<div class="row beta_banner_row">
			<div class="col-lg-6 my-auto">
				<h2>Contact to BlackPineapple:</h2>
			</div>
			<div class="col-lg-6 my-auto">
				<a href="#" class="btn btn-beta"> <i class="fa fa-instagram fa-fw"></i> <span class="network-name">Instagram</span>
				</a> <a href="https://www.facebook.com/bpletsgo/" target="_blank" class="btn btn-beta"> <i class="fa fa-facebook-official fa-fw"></i> <span class="network-name">Facebook</span>
				</a>
			</div>
		</div>
	</div>
</aside>
<!-- /.banner -->

<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>