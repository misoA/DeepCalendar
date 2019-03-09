<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<meta id="_csrf" name="_csrf" content="${_csrf.token}" />
<meta id="_csrf_header" name="_csrf_header"
	content="${_csrf.headerName}" />
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<link
	href='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.min.css'
	rel='stylesheet' />
<link
	href='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.print.min.css'
	rel='stylesheet' media='print' />
<script
	src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/moment.min.js'></script>
<script
	src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/jquery.min.js'></script>
<script
	src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.min.js'></script>


<!-- Page Content -->
<input type="hidden" id="contextPathURL"
	value="${pageContext.request.contextPath}" />

<section class="content-section-a" id="shopping_start">
	<div class="container">
		<h2 class="beta_form_title">Deep Scheduler</h2>
		<div class="row">
			<div class="col-lg-6">
				<form class="form-horizontal page_500" id="moveForm"
					action="${pageContext.request.contextPath}/schedule/updateSchedule"
					method="post">

					<input type="hidden" name="${_csrf.parameterName}"
						value="${_csrf.token}" />
					<div class="form-group flex_form">
						<label class="input-group-text" for="inputGroupSelect01">Type
							: </label> <select class="form-control" id="inputGroupSelect01"
							name="type">
							<c:forEach var="list" items='${type}' varStatus="status">
								<c:if test="${detail.type eq list.codeId}">
								</c:if>
								<c:choose>
									<c:when test="${detail.type eq list.codeId}">
										<option value="${list.codeId}" selected="selected">${list.codeDesc}</option>
									</c:when>
									<c:otherwise>
										<option value="${list.codeId}">${list.codeDesc}</option>
									</c:otherwise>
								</c:choose>
							</c:forEach>
						</select>
					</div>
					<div class="form-group flex_form">
						<label for="inputstdate">FROM : </label>
						<div id="inputstdate" class="alert-danger checkInput"></div>
						<input type="datetime-local" class="form-control" name="stdate"
							value="${start}">
					</div>
					<div class="form-group flex_form">
						<label for="inputstdate">TO : </label>
						<div id="inputstdate" class="alert-danger checkInput"></div>
						<input type="datetime-local" class="form-control" name="enddate"
							value="${end}">
					</div>
					<div class="form-group flex_form">
						<label for="inputaddress">장소 : </label>
						<div id="inputaddress" class="alert-danger checkInput"></div>
						<input type="text" class="form-control" name="address"
							value="${detail.address}">
					</div>
					<div class="form-group flex_form">
						<label for="inputaddress">날씨 : </label>
						<div id="inputaddress" class="alert-danger checkInput"></div>
						<img class="border-radius" src="${detail.weathericon}" />
						<div class="weather-text">${weatherName}</div>
					</div>
					<div class="form-group flex_form">
						<label for="inputstdate">제목 : </label>
						<div id="inputstdate" class="alert-danger checkInput"></div>
						<input type="text" class="form-control" name="title"
							value="${detail.title}">
					</div>
					<div class="form-group flex_form">
						<label for="inputstdate">내용 : </label>
						<div id="inputstdate" class="alert-danger checkInput"></div>
						<textarea class="form-control" name="content">${detail.contents}</textarea>
					</div>
					<div class="form-group flex_form">
						<label for="inputstdate">match : </label>
						<div id="inputstdate" class="alert-danger checkInput"></div>
						<label id="matchRate" class="weather-text"></label>
					</div>
					<input type="hidden" name="calSerialNo"
						value="${detail.calSerialNo}" /> <input type="hidden"
						name="weathericon" value="${detail.weathericon}" />
					<button type="submit" class="btn btn-primary">수정</button>
				</form>
			</div>
			<div class="form-group col-lg-6 container">
				<h4 class="beta_form_title">Recommend Clothes</h4>
				<div class="row">
					<div class="col img150">
						<select id="topList" name="imageUrl"
							class="image-picker show-html">
							<c:forEach var="list" items='${goodsList}' varStatus="status">
								<c:if test="${list.malCf1Name eq 'top'}">
									<option data-img-class="img200" data-img-src="${list.imageUrl}"
										data-code="${list.malCf1Code}" value="${list.imageUrl}">
								</c:if>
							</c:forEach>
						</select>
					</div>
				</div>
				<hr class="intro-divider">
				<div class="row">
					<div class="col img150">
						<select id="bottomList" name="imageUrl"
							class="image-picker show-html">
							<c:forEach var="list" items='${goodsList}' varStatus="status">
								<c:if test="${list.malCf1Name eq 'bottom'}">
									<option data-img-class="img200" data-img-src="${list.imageUrl}"
										data-code="${list.malCf1Code}" value="${list.imageUrl}">
								</c:if>
							</c:forEach>
						</select>
					</div>
				</div>
			</div>
		</div>
		<div class="schedule" id="calendar"></div>
	</div>
</section>


<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy;
			BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>
<script
	src="${pageContext.request.contextPath}/resources/image-picker/image-picker.min.js"></script>
<script
	src="${pageContext.request.contextPath}/resources/js/bp_schedule_detail.js"></script>
