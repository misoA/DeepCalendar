<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>

<!-- Header -->
<header class="intro-header" id="intro-header">
	<div class="container">
		<div class="intro-message">
			<h1>Your Personal AI Stylist</h1>
			<h3>인공지능이 대신 해주는 편한 쇼핑</h3>
			<h3>나의 스타일을 찾아주는 트렌디한 쇼핑</h3>
			<hr class="intro-divider">
		</div>
	</div>
</header>

<!-- Page Content -->
<section class="content-section-a" id="content-section-a">

	<div class="container">
		<div class="row">
			<div class="col-lg-5 ml-auto">
				<hr class="section-heading-spacer">
				<div class="clearfix"></div>
				<h2 class="section-heading">
					BlackPineapple:<br>서비스
				</h2>
				<p class="lead">
					인공지능 알고리즘과 전문 스타일리스트의 콜라보레이션을 통해 고객에게 가장 필요한 패션 아이템을 추천합니다.<br> <br> 이런 분들은 이용해보세요 : <br> ▹쇼핑을 하는 것이
					싫고, 귀찮은 사람 <br> ▹너무 바빠서 쇼핑을 할 시간이 없는 사람 <br> ▹평소에 입는 스타일이 아닌 새로운 패션을 추천 받고 싶은 사람 <br>
				</p>
			</div>
			<div class="col-lg-5 mr-auto">
				<img class="img-fluid" src="${pageContext.request.contextPath}/resources/img/style_a.jpg" alt="">
			</div>
		</div>

	</div>
	<!-- /.container -->
</section>

<section class="content-section-b" id="content-section-b">

	<div class="container">

		<div class="row">
			<div class="col-lg-5 mr-auto order-lg-2">
				<hr class="section-heading-spacer">
				<div class="clearfix"></div>
				<h2 class="section-heading">이용방법</h2>
				<p class="lead">
					1. 블랙파인애플 쇼핑몰에 접속한다<br> 2. 회원가입을 한다<br> 3. 옷이 배송되길 기다린다<br> 4. 배송된(블랙파인애플이 추천한) 옷을 입어본다<br> 5.
					마음에 드는 옷을 구매한다<br> ※ 마음에 들지않는 옷은 무료로 반품한다
				</p>
			</div>
			<div class="col-lg-5 ml-auto order-lg-1">
				<img class="img-fluid" src="${pageContext.request.contextPath}/resources/img/style_b.jpg" alt="">
			</div>
		</div>

	</div>
	<!-- /.container -->

</section>
<!-- /.content-section-b -->

<section class="content-section-a">

	<div class="container">

		<div class="row">
			<div class="col-lg-5 ml-auto">
				<hr class="section-heading-spacer">
				<div class="clearfix"></div>
				<h2 class="section-heading">서비스 출시</h2>
				<p class="lead">
					2018년 상반기 정식 서비스가 런칭됩니다. <br> <a href="${pageContext.request.contextPath}/bpbeta/notice#shopping_notice">서비스
						알림 등록하러가기</a><br> <br> 2017년 12월 <a href="http://app-show.co.kr/blackpineapple-c09-2017/" target="_blank">제4회
						App Show Korea</a>를 통해 베타테스트 서비스를 선보였습니다.

				</p>
			</div>
			<div class="col-lg-5 mr-auto ">
				<img class="img-fluid" src="${pageContext.request.contextPath}/resources/img/style_c.jpg" alt="">
			</div>
		</div>

	</div>
	<!-- /.container -->

</section>

<section class="content-section-b" id="content-section-b">
	<div class="container">
		<div class="row">
			<div class="col-lg-10 mr-auto order-lg-2">
				<hr class="section-heading-spacer">
				<div class="clearfix"></div>
				<h2 class="section-heading">Beta 서비스가 시작되면 메일로 알려드립니다</h2>
				<div class="row">
					<div class="col-lg-2"></div>
					<div class="col-lg-10 form_div">
						<form role="form" id="noticeMailForm" method="POST"
							action="${pageContext.request.contextPath}/data/noticeMailSend" accept-charset="UTF-8">
							<div class="form-group">
								<label for="inputEmail">이메일</label>
								<div id="inputEmailCheck" class="alert-danger checkInput"></div>
								<input type="text" class="form-control" id="inputEmail" name="inputEmail" placeholder="알림받을 메일 주소를 적어주세요">
							</div>
							<div class="form-group">
								<label for="inputContents">Contact</label>
								<textarea cols="10" rows="10" class="form-control" id="inputContents" name="inputContents"
									placeholder="블랙파인애플 팀에게 하고 싶은 이야기를 적어주세요"></textarea>
							</div>
						</form>
						<button type="button" class="btn btn-beta-next" id="noticeMailSubmitBtn">
							알림 받기 <i class="fa fa-fighter-jet"></i>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<section class="content-section-b" id="content-team">
	<div class="container">
		<div class="row">
			<div class="col-lg-8 mr-auto order-lg-2">
				<hr class="section-heading-spacer">
				<div class="clearfix"></div>
				<h2 class="section-heading">BlackPineapple Team</h2>
				<p class="lead">
					<b>당신만의 인공지능 스타일리스트 BlackPineapple.</b><br> 블랙파인애플 팀은 고객 모두가 자신만의 패션 스타일을 가지고, 그 안에서 '트렌디'함을 찾는 것을 지향합니다.
				</p>
			</div>
		</div>
	</div>
	<div class="container">
		<div class="row team-row">
			<div class="col-lg-3">
				<img class="img-circle" src="${pageContext.request.contextPath}/resources/img/ceo.jpg"
					alt="Generic placeholder image" width="200" height="200">
				<h3>박미소 (CEO)</h3>
				<p>
					▹ General Develop Manager<br>
				</p>
			</div>
			<div class="col-lg-3">
				<img class="img-circle" src="${pageContext.request.contextPath}/resources/img/coo.jpg"
					alt="Generic placeholder image" width="200" height="200">
				<h3>김지수 (COO)</h3>
				<p>
					▹ General Design Manager<br>
				</p>
			</div>
			<div class="col-lg-3">
				<img class="img-circle" src="${pageContext.request.contextPath}/resources/img/pineapple.jpg"
					alt="Generic placeholder image" width="200" height="200">
				<h3>Open For You</h3>
				<p>
					▹ Our Next Member<br>
				</p>
			</div>
			<div class="col-lg-3">
				<img class="img-circle" src="${pageContext.request.contextPath}/resources/img/pineapple.jpg"
					alt="Generic placeholder image" width="200" height="200">
				<h3>Open For You</h3>
				<p>
					▹ Our Next Member<br>
				</p>
			</div>
		</div>
	</div>
</section>

<aside class="banner" id="snsbanner">

	<div class="container">

		<div class="row">
			<div class="col-lg-6 my-auto">
				<h2>Contact to BlackPineapple:</h2>
			</div>
			<div class="col-lg-6 my-auto">
				<ul class="list-inline banner-social-buttons">
					<li class="list-inline-item">
						<a href="#" class="btn btn-secondary btn-lg"> <i class="fab fa-instagram"></i> <span class="network-name">Instagram</span>
						</a>
					</li>
					<li class="list-inline-item">
						<a href="https://www.facebook.com/bpletsgo/" target="_blank" class="btn btn-secondary btn-lg"> <i
							class="fab fa-facebook"></i> <span class="network-name">Facebook</span>
						</a>
					</li>
				</ul>
			</div>
		</div>

	</div>
	<!-- /.container -->
</aside>
<!-- /.banner -->

<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>