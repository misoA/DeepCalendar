<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="tiles" uri="http://tiles.apache.org/tags-tiles"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html>
<head>
<tiles:insertAttribute name="header" />
<title><tiles:insertAttribute name="header_title" /></title>
</head>

<body>
	<!-- Global site tag (gtag.js) - Google Analytics -->
	<script async src="https://www.googletagmanager.com/gtag/js?id=UA-115476238-1"></script>
	<script>
		window.dataLayer = window.dataLayer || [];
		function gtag() {
			dataLayer.push(arguments);
		}
		gtag('js', new Date());

		gtag('config', 'UA-115476238-1');
	</script>

	<tiles:insertAttribute name="body" />
	<tiles:insertAttribute name="footer_script" />
	<tiles:insertAttribute name="modal" />
</body>
</html>