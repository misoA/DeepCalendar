package com.blackpineapple.web.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

/**
 * Handles requests for the application home page.
 */
@Controller
@RequestMapping(value = "/bpbeta")
public class BpBetaPageController {

	private static final Logger	logger				= LoggerFactory.getLogger(BpBetaPageController.class);


	/**
	 * Main Page
	 * 
	 * @return
	 */
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String bpbeta() {
		return "/views/bpbeta";
	}
	

	/**
	 * Notice Page
	 * 
	 * @return
	 */
	@RequestMapping(value = "/notice", method = RequestMethod.GET)
	public String bpbetaNotice() {
		return "/views/bpbeta_notice";
	}

}
