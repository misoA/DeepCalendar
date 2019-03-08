package com.blackpineapple.web.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.SessionAttributes;
import org.springframework.web.servlet.ModelAndView;

import com.blackpineapple.web.service.user.UserAuthServiceImple;
import com.blackpineapple.web.vo.UserInfoVO;

/**
 * Handles requests for the application home page.
 */
@Controller
@SessionAttributes("user")
@RequestMapping(value = "/login")
public class LoginController {

	private static final Logger		logger	= LoggerFactory.getLogger(LoginController.class);

	@Autowired
	private UserAuthServiceImple	userAuthService;


	/**
	 * login Page
	 * 
	 * @return
	 */
	@RequestMapping(value = "/page", method = RequestMethod.GET)
	public ModelAndView loginPage() {
		ModelAndView mav = new ModelAndView("/views/login");
		mav.addObject("page", "login");
		return mav;
	}
	
	@RequestMapping(value = "/join", method = RequestMethod.GET)
	public ModelAndView joinPage() {
		ModelAndView mav = new ModelAndView("/views/bpbeta");
		return mav;
	}

	/**
	 * Spring Security Login Success
	 * 
	 * @param model
	 * @param auth
	 * @return
	 */
	@RequestMapping(value = "/success", method = RequestMethod.GET)
	public ModelAndView loginSuccess(Model model, Authentication auth) {
		logger.info("Login Success");
		// 반환할 유저정보
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		model.addAttribute("user", userInfo);
		ModelAndView mav = new ModelAndView("/views/bpschedule");
		return mav;
	}

	/**
	 * Spring Security Login Duplicate
	 * 
	 * @return
	 */
	@RequestMapping(value = "/duplicate", method = RequestMethod.GET)
	public String loginDuplicate() {
		logger.info("login_duplicate!");
		return "redirect:/";
	}

	/**
	 * Spring Security Login Fail
	 * 
	 * @return
	 */
	@RequestMapping(value = "/fail", method = RequestMethod.GET)
	public ModelAndView loginFail() {
		ModelAndView mav = new ModelAndView("/views/loginFail");
		mav.addObject("page", "login");
		logger.info("login_fail!");
		return mav;
	}

}
