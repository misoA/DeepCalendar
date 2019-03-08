package com.blackpineapple.web.controller;

import java.io.File;
import java.io.IOException;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.SessionAttributes;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.servlet.ModelAndView;

import com.amazonaws.services.s3.model.ObjectMetadata;
import com.blackpineapple.dao.generate.model.Closet;
import com.blackpineapple.dao.generate.model.GoodsTag;
import com.blackpineapple.web.service.ClosetServiceImple;
import com.blackpineapple.web.service.FileUploadSeviceImple;
import com.blackpineapple.web.service.HttpConnectionUtil;
import com.blackpineapple.web.service.user.UserAuthServiceImple;
import com.blackpineapple.web.vo.UserInfoVO;
import com.fasterxml.jackson.core.JsonParser.Feature;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

/**
 * Handles requests for the application home page.
 */
@Controller
@SessionAttributes("user")
@RequestMapping(value = "/closet")
@PropertySource("classpath:config/properties/web.ALL.properties")
public class ClosetController {

	private static final Logger	logger				= LoggerFactory.getLogger(ClosetController.class);
	
	@Autowired
	private ClosetServiceImple closetService;
	
	@Autowired
	private UserAuthServiceImple	userAuthService;
	
	@Autowired
	private FileUploadSeviceImple fileUploadSeviceImple;
	
	@Value("${image.api.url}")
	private String apiUrl;
	
	
	/**
	 * Main Page
	 * 
	 * @return
	 */
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String getCloset() {
		return "/views/bpcloset";
	}
	
	@RequestMapping(value = "/get", method = RequestMethod.GET)
	@ResponseBody
	public List<Map> getCloset(Authentication auth) {
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		List<Map> list = closetService.getClosetByUser(userInfo);
		
		return list;
	}
	
	@RequestMapping(value = "/insertPage", method = RequestMethod.GET)
	public String moveinsert() {
		return "/views/bpcloset_insert";
	}
	
	@RequestMapping(value = "/imageUpload", method = RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> imageUpload( MultipartFile uploadfile) throws IOException {
		ObjectMetadata metadata = new ObjectMetadata();
		String url = fileUploadSeviceImple.uploadFile(uploadfile, "bpcalender", metadata);
		
		String result = HttpConnectionUtil.connectHttpGet(apiUrl+"/detectImage?detectImName=" + url);
		ObjectMapper mapper = new ObjectMapper();
		logger.info(result);
		mapper.configure(DeserializationFeature.ACCEPT_SINGLE_VALUE_AS_ARRAY, true);
		Map<String, Object> map = mapper.readValue(result, new TypeReference<Map<String, Object>>() {});

		return map;
	}
	
	@RequestMapping(value = "/insertCloset", method = RequestMethod.POST)
	public String insertCloset(Authentication auth, @RequestParam (name = "name") String name, String imageUrl) throws IllegalStateException, IOException {
		
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		// Closet VO
		Closet closet = new Closet();
		closet.setBpCustomerId(userInfo.getId());
		closet.setName(name);
		closet.setImageUrl(imageUrl);
		closet.setCreateDate(new Date());
		
		String imageName = "";
		int i = imageUrl.lastIndexOf("/");
		imageName = imageUrl.substring(i+1);
		
		String result = HttpConnectionUtil.connectHttpGet(apiUrl+"/ClassificateImage?imName=" + imageName);
		ObjectMapper mapper = new ObjectMapper();
		Map<String, Object> map = mapper.readValue(result, new TypeReference<Map<String, Object>>() {});
		
		Closet insCloset = closetService.insertCloset(closet);
		closetService.insertClothesCodeTag(map, insCloset.getSerialNo());
		
		return "redirect:/closet/";
	}
	
	@RequestMapping(value = "/updateCloset", method = RequestMethod.POST)
	public ModelAndView updateCloset(Authentication auth, @RequestParam(name = "calSerialNo") String calSerialNo, @RequestParam(name = "stdate") String stdate, @RequestParam(name = "enddate") String enddate,
			@RequestParam(name = "title") String title, @RequestParam(name = "content") String content) {
		
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		
		// Closet VO
		Closet closet = new Closet();
		closet.setBpCustomerId(userInfo.getId());
		
		closetService.updateCloset(closet);
		
		ModelAndView mav = new ModelAndView("/views/bpCloset");
		return mav;
	}

}
