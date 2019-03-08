<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<meta id="_csrf" name="_csrf" content="${_csrf.token}"/>
<meta id="_csrf_header" name="_csrf_header" content="${_csrf.headerName}"/>
<link href='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.min.css' rel='stylesheet' />
<link href='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.print.min.css' rel='stylesheet' media='print' />
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/moment.min.js'></script>
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/jquery.min.js'></script>
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/fullcalendar.min.js'></script>


<!-- Page Content -->
<input type="hidden" id="contextPathURL" value="${pageContext.request.contextPath}" />

<section class="content-section-a calendar-bg" id="shopping_start">
	<div class="container">
		<div class="schedule" id = "calendar">
		</div>
	</div>
</section>
<form class="form-horizontal d-none" id="moveForm" action="${pageContext.request.contextPath}/schedule/insert" method="POST">
	<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" />
	<input type="datetime-local" name="selectDate" id="selectDate" value="" />
	<input type="hidden" name="calSerialNo" id="calSerialNo" value="" />
</form>


<!-- /.banner -->

<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>

<script src="${pageContext.request.contextPath}/resources/js/bp_schedule.js"></script>