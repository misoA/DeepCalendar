package com.blackpineapple.web.service.user;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.authentication.dao.ReflectionSaltSource;
import org.springframework.security.authentication.dao.SaltSource;
import org.springframework.security.authentication.encoding.ShaPasswordEncoder;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

public class CustomAuthenticationProvider implements AuthenticationProvider {

	private static final Logger		logger	= LoggerFactory.getLogger(CustomAuthenticationProvider.class);

	@Autowired
	private UserAuthServiceImple	authService;

	@Override
	public Authentication authenticate(Authentication authentication) throws AuthenticationException {

		String id = (String) authentication.getPrincipal();
		String password = (String) authentication.getCredentials();

		logger.info("Welcome authenticate! {}", id);
		
		SaltSource saltSource2 = new ReflectionSaltSource();
		String encodePassword = new ShaPasswordEncoder(256).encodePassword(password, saltSource2);
		logger.info("Welcome authenticate! {}", encodePassword);
		
		try {
			// check whether user's credentials are valid.
			UserDetails loadUserByUsername = authService.loadUserByUsername(id);

			SaltSource saltSource = new ReflectionSaltSource();
			logger.info("Welcome authenticate! {}", password + "//" + loadUserByUsername.getPassword());
			if (new ShaPasswordEncoder(256).isPasswordValid(loadUserByUsername.getPassword(), password, saltSource)) {
				UsernamePasswordAuthenticationToken result = new UsernamePasswordAuthenticationToken(id, password, loadUserByUsername.getAuthorities());
				return result;
			} else {
				throw new BadCredentialsException("AbstractUserDetailsAuthenticationProvider.badCredentials");
			}
		} catch (UsernameNotFoundException e) {
			logger.error(e.toString());
			throw new UsernameNotFoundException(e.getMessage());
		} catch (BadCredentialsException e) {
			logger.error(e.toString());
			throw new BadCredentialsException(e.getMessage());
		} catch (Exception e) {
			logger.error(e.toString());
			throw new RuntimeException(e.getMessage());
		}
	}

	@Override
	public boolean supports(Class<?> authentication) {
		return true;
	}

}
