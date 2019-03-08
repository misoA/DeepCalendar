package com.blackpineapple.web.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.mail.MessagingException;
import javax.mail.internet.AddressException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.dao.ReflectionSaltSource;
import org.springframework.security.authentication.dao.SaltSource;
import org.springframework.security.authentication.encoding.ShaPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import com.blackpineapple.dao.generate.model.BPCustomer;
import com.blackpineapple.web.service.DataService;
import com.blackpineapple.web.service.EmailService;
import com.blackpineapple.web.vo.ClothesVO;

/**
 * Handles requests for the application home page.
 */
@Controller
@RequestMapping(value = "/data")
public class DataController {

	private static final Logger	logger	= LoggerFactory.getLogger(DataController.class);

	@Autowired
	private DataService			dataService;

	@Autowired
	private EmailService		mailService;

	@RequestMapping(value = "/customerDuplicate", method = RequestMethod.POST)
	public @ResponseBody String customerDuplicate(@RequestParam(name = "nickname") String nickname, @RequestParam(name = "id") String id) {
		boolean nicknameDuplicate = dataService.nicknameDuplicate(nickname);
		boolean idDuplicate = dataService.idDuplicate(id);
		if (nicknameDuplicate && idDuplicate) {
			return "both";
		} else if (nicknameDuplicate) {
			return "nick";
		} else if (idDuplicate) {
			return "id";
		} else {
			return "ok";
		}
	}

	@RequestMapping(value = "/insertCustomer", method = RequestMethod.POST)
	public ModelAndView insertCustomer(@RequestParam(name = "inputId") String inputId, @RequestParam(name = "inputPassword") String inputPassword,
					@RequestParam(name = "inputNickname") String inputNickname, @RequestParam(name = "inputShirt") String inputShirt,
					@RequestParam(name = "inputPants") String inputPants, @RequestParam(name = "inputHeight") String inputHeight,
					@RequestParam(name = "inputWeight") String inputWeight, @RequestParam(name = "inputRemark", defaultValue = "") String inputRemark) {

		// Password 인코딩
		SaltSource saltSource = new ReflectionSaltSource();
		String encodePassword = new ShaPasswordEncoder(256).encodePassword(inputPassword, saltSource);

		ModelAndView mav = new ModelAndView("/views/bpbeta2");
		BPCustomer customer = dataService.insertCustomer(inputId, encodePassword, inputNickname, inputShirt, inputPants, inputHeight, inputWeight, inputRemark);
		mav.addObject("customer", customer);
		mav.addObject("categoryList", dataService.getStyleCategoryCodeList());
		mav.addObject("clothesList", dataService.getRandomClothesList());
		mav.addObject("page", "1");
		return mav;
	}

	@RequestMapping(value = "/insertCustomerStyle", method = RequestMethod.POST)
	public ModelAndView insertCustomerStyle(@RequestParam Map<String, String> allRequestParams) {
		logger.info("Start insertCustomerStyle");
		List<ClothesVO> clothesList = new ArrayList<ClothesVO>();
		String usualStyleCode = "", usualStyleName = "", wantedStyleCode = "", wantedStyleName = "";

		// 파라미터 파싱
		for (String key : allRequestParams.keySet()) {
			String[] keys = key.split(",");
			if (keys[0].equals("id")) {
				String[] values = allRequestParams.get(key).split(",");
				String malCf1Code = values[0];
				String malCf1Name;
				if (malCf1Code.equals("RE_1")) {
					malCf1Name = "musinsa";
				} else {
					malCf1Name = "sinsangmarket";
				}
				clothesList.add(Integer.parseInt(keys[1]) - 1, new ClothesVO(Integer.parseInt(values[1]), malCf1Code, malCf1Name));
			} else if (keys[0].equals("rating")) {
				ClothesVO clothesVO = clothesList.get(Integer.parseInt(keys[1]) - 1);
				clothesVO.setRating(Integer.parseInt(allRequestParams.get(key)));
			} else if (keys[0].equals("1")) {
				usualStyleCode = keys[1];
				usualStyleName = allRequestParams.get(key);
			} else if (keys[0].equals("2")) {
				wantedStyleCode = keys[1];
				wantedStyleName = allRequestParams.get(key);
			}
		}
		// Rating 입력
		dataService.insertClothesStars(allRequestParams.get("customerId"), clothesList, usualStyleCode, usualStyleName, wantedStyleCode, wantedStyleName);
		
		ModelAndView mav = new ModelAndView("/views/bpbeta2");
		mav.addObject("page", "2");
		mav.addObject("customerNickName", allRequestParams.get("customerNickname"));
		logger.info("END insertCustomerStyle");
		return mav;
	}

	@RequestMapping(value = "/noticeMailSend", method = RequestMethod.POST)
	public String noticeMailSend(@RequestParam(name = "inputEmail") String email, @RequestParam(name = "inputContents", required = false, defaultValue = "text") String contents)
					throws AddressException, MessagingException {
		logger.info("START noticeMailSend");
		try {
			mailService.sendBetaNoticeEmail(email, contents);
		} catch (MessagingException e) {
			e.printStackTrace();
		}
		logger.info("END noticeMailSend");
		return "/views/bpinfo";
	}

}
