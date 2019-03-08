<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<meta id="_csrf" name="_csrf" content="${_csrf.token}"/>
<meta id="_csrf_header" name="_csrf_header" content="${_csrf.headerName}"/>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<link href='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.min.css' rel='stylesheet' />
<link href='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.print.min.css' rel='stylesheet' media='print' />
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/moment.min.js'></script>
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/jquery.min.js'></script>
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.min.js'></script>


<!-- Page Content -->
<input type="hidden" id="contextPathURL" value="${pageContext.request.contextPath}" />

<section class="content-section-a" id="shopping_start">
	<div class="container">
		<h2 class="beta_form_title">Deep Scheduler</h2>
			<form class="form-horizontal page_500" id="moveForm" action="${pageContext.request.contextPath}/schedule/insertSchedule" method="post">
				<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" />
				<div class="form-group flex_form">
					<label class="input-group-text" for="inputGroupSelect01">Type : </label>
					<select class="form-control" id="inputGroupSelect01" name="type">
						<c:forEach var = "list" items = '${type}' varStatus = "status">
							<option value="${list.codeId}">${list.codeDesc}</option>
						</c:forEach>	
					</select>
				</div>
				
				<div class="form-group flex_form">
					<label for="inputstdate">FROM : </label>
					<div id="inputstdate" class="alert-danger checkInput"></div>
					<input type="datetime-local" class="form-control" name="stdate" value="${insertDate}">
				</div>
				<div class="form-group flex_form">
					<label for="inputstdate">TO : </label>
					<div id="inputstdate" class="alert-danger checkInput"></div>
					<input type="datetime-local" class="form-control" name="enddate" value="">
				</div>
				<div class="form-group flex_form">
					<label for="inputaddress">장소 : </label>
					<div id="inputaddress" class="alert-danger checkInput"></div>
					<input type="text" class="form-control" name="address" value="">
				</div>
				<div class="form-group flex_form">
					<label for="inputstdate">제목 : </label>
					<div id="inputstdate" class="alert-danger checkInput"></div>
					<input type="text" class="form-control" name="title" value="">
				</div>
				<div class="form-group flex_form">
					<label for="inputstdate">내용 : </label>
					<div id="inputstdate" class="alert-danger checkInput"></div>
					<textarea class="form-control" name="content"></textarea>
				</div>
				<div class="form-group flex_form">
					<button type="submit" class="btn btn-primary">입력</button>
				</div>
			</form>
		<div class="schedule" id = "calendar">
		</div>
	</div>
</section>


<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>

<%-- <script src="${pageContext.request.contextPath}/resources/js/bp_schedule.js"></script> --%>