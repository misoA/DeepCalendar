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
@RequestMapping(value = "/bpinfo")
public class BpInfoPageController {

	private static final Logger	logger				= LoggerFactory.getLogger(BpInfoPageController.class);


	/**
	 * Main Page
	 * 
	 * @return
	 */
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String bpinfo() {
		return "/views/bpinfo";
	}

}
