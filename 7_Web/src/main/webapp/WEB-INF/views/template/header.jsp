<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="icon" type="image/png" href="${pageContext.request.contextPath}/resources/img/papng.png" />

<!-- calendar -->
<link href="${pageContext.request.contextPath}/resources/css/datepicker3.css" rel="stylesheet">
<link href="${pageContext.request.contextPath}/resources/image-picker/image-picker.css" rel="stylesheet">

<!-- Custom styles for this template -->
<link href="${pageContext.request.contextPath}/resources/css/landing-page.css" rel="stylesheet">
<link href="${pageContext.request.contextPath}/resources/css/beta-page.css" rel="stylesheet">

<!-- Navigation -->
<%@ taglib uri="http://www.springframework.org/security/tags" prefix="sec" %>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
	<div class="container">
		<a class="navbar-brand" href="${pageContext.request.contextPath}/">
		<img class="nav-logo" src="${pageContext.request.contextPath}/resources/img/logo/PNG/bp_logo.png"
					alt="LOGO"> </a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive"
			aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarResponsive">
			<ul class="navbar-nav ml-auto">
				<li class="nav-item">
					<a class="nav-link" href="${pageContext.request.contextPath}/bpinfo/">About</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="${pageContext.request.contextPath}/closet/">Closet</a>
				</li>
				<sec:authorize access="isAnonymous()">
				</sec:authorize>
				<sec:authorize access="isAuthenticated()">
					<li class="nav-item">
						<a class="nav-link" onclick="document.getElementById('logout-form').submit();" href="#">Logout</a>
					</li>
				</sec:authorize>
			</ul>
		</div>

		<form id="logout-form" action="${pageContext.request.contextPath}/login/logout" method="post">
		    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
		</form>
	</div>
</nav>


