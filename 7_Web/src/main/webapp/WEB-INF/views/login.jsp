<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>

<header class="intro-header" id="intro-header">
	<div class="container">
		<div class="intro-message">
			<h1>FASHION BASED ON SCHEDULE</h1><br>
			<h3>인공지능이 대신 해주는 편한 쇼핑</h3>
			<h3>나의 스타일을 찾아주는 트렌디한 쇼핑</h3>
			<form class="form-signin" action="${pageContext.request.contextPath}/login/login" method="post">
					<fieldset>
						<div class="input-prepend" title="username">
							<span class="add-on">
								<i class="icon-user"></i>
							</span>
							<input class="form-control" name="id" id="id" type="text" placeholder="아이디 입력" />
						</div>
						<div class="clearfix"></div>

						<div class="input-prepend" title="password">
							<span class="add-on">
								<i class="icon-lock"></i>
							</span>
							<input class="form-control" name="password" id="password" type="password" placeholder="비밀번호 입력" />
						</div>
						<div class="clearfix"></div>
						<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" />
						<div class="btn btn-lg btn-primary btn-block">
							<button type="submit" class="btn btn-primary">로그인</button><br/>
							<a href = "${pageContext.request.contextPath}/login/join"><button type="button" class="btn btn-primary">회원가입</button></a>
						</div>
						<div class="clearfix"></div>
					</fieldset>
				</form>
		</div>
	</div>
</header>

<!--/.fluid-container-->