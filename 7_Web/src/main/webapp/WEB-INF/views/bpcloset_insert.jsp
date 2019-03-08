<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<meta id="_csrf" name="_csrf" content="${_csrf.token}"/>
<meta id="_csrf_header" name="_csrf_header" content="${_csrf.headerName}"/>
<script src='${pageContext.request.contextPath}/resources/fullcalendar-3.9.0/lib/jquery.min.js'></script>


<!-- Page Content -->
<input type="hidden" id="contextPathURL" value="${pageContext.request.contextPath}" />


<section class="content-section-a" id="shopping_start">
	<div class="container">
		<h2 class="beta_form_title">Closet</h2>
<%-- 		<form class="form-horizontal" id="moveForm" action="${pageContext.request.contextPath}/closet/insertCloset" method="post" enctype="multipart/form-data"> --%>
<%-- 				<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" /> --%>
<!-- 				<input type="text" name="name" value="" /> -->
<!-- 				<input type="file" name="uploadfile" placeholder="파일 선택" /><br/> -->
<!-- 				<button type="submit" class="btn btn-primary">업로드</button> -->
<%-- 		</form> --%>
		<form:form class="form-horizontal page_800" id="moveForm" action="${pageContext.request.contextPath}/closet/insertCloset" method="post">
			<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" />
			<div class="form-group flex_form">
				<label for="inputName">사진 : </label>
				<input type="file" name="uploadfile" id="imageFile" placeholder="파일 선택" />
				<button type="button" class="btn btn-primary" id = "imageUpload">이미지업로드</button>
			</div>
			<div class="form-group flex_form">
				<select id="imageList" name="imageUrl" class="image-picker show-html d-none"></select>
			</div>
			<div class="form-group flex_form">
				<label for="inputName">이름 : </label>
				<input type="text" name="name" value="" class="form-control" />
			</div>
			<button type="submit" class="btn btn-primary">저장</button>
		</form:form>
	</div>
</section>

<script src="${pageContext.request.contextPath}/resources/image-picker/image-picker.min.js"></script>
<script src="${pageContext.request.contextPath}/resources/js/bp_closet_insert.js"></script>
<!-- /.banner -->

<!-- Footer -->
<footer>
	<div class="container">
		<p class="copyright text-muted small">Copyright &copy; BlackPineapple. miso All Rights Reserved</p>
	</div>
</footer>

