<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<meta id="_csrf" name="_csrf" content="${_csrf.token}"/>
<meta id="_csrf_header" name="_csrf_header" content="${_csrf.headerName}"/>
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/jquery.min.js'></script>


<!-- Page Content -->
<input type="hidden" id="contextPathURL" value="${pageContext.request.contextPath}" />

<section class="content-section-a" id="shopping_start">
	<div class="container">
		<h2 class="beta_form_title">Closet</h2>
		<h2 class="beta_form_title">옷목록</h2>
		<a href="${pageContext.request.contextPath}/closet/insertPage"><button type="button" class="btn btn-primary">+</button></a>
		<div class="row beta_columns img200" id="closet_list">
		</div>
	</div>
</section>

<!-- /.banner -->

<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>

<script src="${pageContext.request.contextPath}/resources/js/bp_closet.js"></script>