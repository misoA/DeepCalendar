<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<div id="wrap">
	<!--loading-->
	<section class="loading">
		<p>
			<strong id="loding_beta_text">Loading ... </strong>
		</p>
	</section>
</div>

<input type="hidden" id="contextPathURL" value="${pageContext.request.contextPath}" />
<section class="content-section-a" id="shopping_start">
	<div class="container">
		<h2 class="beta_form_title">BlackPineapple_Beta</h2>
		<c:if test="${page eq 1}">
			<form role="form" id="styleForm" method="POST" action="${pageContext.request.contextPath}/data/insertCustomerStyle"
				accept-charset="UTF-8">
				<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" />
				<input type="hidden" class="form-control" id="customerId" name="customerId" value="${customer.bpCustomerId}">
				<input type="hidden" class="form-control" id="customerNickname" name="customerNickname"
					value="${customer.bpCustomerNickname}">
				<div id="styleSubmit1">
					<h5 class="image-radio-title">${customer.bpCustomerNickname}님이 평소에 즐겨입는 스타일의 옷을 골라주세요</h5>
					<div class="beta_columns">
						<c:forEach var="list" items="${clothesList}" varStatus="stat">
							<c:if test="${stat.count <= 15}">
								<figure>
									<img src="${list.goodsImage}" alt="${list.goodsName}">
									<input type="hidden" id="id,${stat.count}" name="id,${stat.count}" value="${list.malCf1Code},${list.goodsId}">
									<input type="hidden" id="rating,${stat.count}" name="rating,${stat.count}" value="1">
								</figure>
							</c:if>
						</c:forEach>
					</div>
					<div class="modal-footer item-beta-footer" id="joinModalFooter">
						<button type="button" class="btn btn-beta-next" id="styleSubmitBtn1">
							다음페이지 <i class="fa fa-fighter-jet"></i>
						</button>
					</div>
				</div>
				<div id="styleSubmit2">
					<div class="row beta_form_row"></div>
					<h5 class="image-radio-title">${customer.bpCustomerNickname}님이 자주 입는 스타일 알려주세요</h5>
					<div class="form-group image-radio-form">
						<c:forEach var="list" items="${categoryList}" varStatus="stat">
							<div class="box">
								<label class="btn image-radio-btn"> <img
									src="${pageContext.request.contextPath}/resources/img/style_category/${list.codeName}.PNG"
									alt="${list.codeName}" class="img-thumbnail img-check"> <br>${list.codeName} - ${list.codeDesc}<br>
									<input type="radio" id="1,ST_${stat.count}" name="1,ST_${stat.count}" value="${list.codeName}" class="hidden"
									autocomplete="off">
								</label>
							</div>
						</c:forEach>
					</div>

					<h5 class="image-radio-title">${customer.bpCustomerNickname}님이 도전하고 싶은 스타일 알려주세요</h5>
					<div class="form-group image-radio-form">
						<c:forEach var="list" items="${categoryList}" varStatus="stat">
							<div class="box">
								<label class="btn image-radio-btn"> <img
									src="${pageContext.request.contextPath}/resources/img/style_category/${list.codeName}.PNG"
									alt="${list.codeName}" class="img-thumbnail img-check2"> <br>${list.codeName} - ${list.codeDesc}<br>
									<input type="radio" id="2,ST_${stat.count}" name="2,ST_${stat.count}" value="${list.codeName}" class="hidden"
									autocomplete="off">
								</label>
							</div>
						</c:forEach>
					</div>
					<div class="modal-footer item-beta-footer" id="joinModalFooter">
						<button type="button" class="btn btn-beta-next" id="styleSubmitBtn2">
							다음페이지 <i class="fa fa-fighter-jet"></i>
						</button>
					</div>
				</div>
				<div id="styleSubmit3">
					<h5 class="image-radio-title">${customer.bpCustomerNickname}님이 구입하고 싶은 옷의 점수를 매겨주세요</h5>
					<div class="beta_columns">
						<c:forEach var="list" items="${clothesList}" varStatus="stat">
							<c:if test="${stat.count > 15}">
								<figure>
									<img src="${list.goodsImage}" alt="${list.goodsName}">
									<input type="hidden" class="form-control" id="id,${stat.count}" name="id,${stat.count}"
										value="${list.malCf1Code},${list.goodsId}">
									<figcaption>
										<select class="form-control star-select" id="rating,${stat.count}" data-rel="chosen"
											name="rating,${stat.count}" required="required">
											<option value="1">★☆☆☆☆</option>
											<option value="2">★★☆☆☆</option>
											<option value="3">★★★☆☆</option>
											<option value="4">★★★★☆</option>
											<option value="5">★★★★★</option>
										</select>
									</figcaption>
								</figure>
							</c:if>
						</c:forEach>
					</div>
					<div class="modal-footer item-beta-footer" id="joinModalFooter">
						<button type="button" class="btn btn-beta-next" id="styleSubmitBtn4">
							회원가입완료 <i class="fa fa-gift"></i>
						</button>
					</div>
				</div>
			</form>
		</c:if>
		<c:if test="${page eq 2}">
			<img class="img-fluid last-join-image" src="${pageContext.request.contextPath}/resources/img/logo/PNG/BLACKPINEAPPLE_WHITE_02.png"
					alt="LOGO">
			<h5 class="beta_form_title">${customerNickName}님 가입해주셔서 감사합니다.</h5>
			<div class="modal-footer" id="joinModalFooter">
				<a href="${pageContext.request.contextPath}/" class="btn btn-beta-next" id="styleSubmitBtn"> 홈으로 <i
					class="fa fa-home"></i>
				</a>
			</div>
		</c:if>
	</div>
</section>

<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>

<script src="${pageContext.request.contextPath}/resources/vendor/jquery/jquery.min.js"></script>
