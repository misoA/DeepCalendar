package com.blackpineapple.web.controller;

import java.io.IOException;
import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Map;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.dao.ReflectionSaltSource;
import org.springframework.security.authentication.dao.SaltSource;
import org.springframework.security.authentication.encoding.ShaPasswordEncoder;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.SessionAttributes;
import org.springframework.web.servlet.ModelAndView;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import com.blackpineapple.dao.generate.model.BPCustomer;
import com.blackpineapple.dao.generate.model.Calendar;
import com.blackpineapple.dao.generate.model.Code;
import com.blackpineapple.dao.generate.model.WeatherCode;
import com.blackpineapple.web.service.HttpConnectionUtil;
import com.blackpineapple.web.service.ScheduleServiceImple;
import com.blackpineapple.web.service.user.UserAuthServiceImple;
import com.blackpineapple.web.vo.UserInfoVO;

/**
 * Handles requests for the application home page.
 */
@Controller
@SessionAttributes("user")
@RequestMapping(value = "/schedule")
public class ScheduleController {

	private static final Logger	logger				= LoggerFactory.getLogger(ScheduleController.class);
	
	@Autowired
	private ScheduleServiceImple schedule;
	
	@Autowired
	private UserAuthServiceImple	userAuthService;

	private String apiServer = ""
	private String weatherServer = ""
	/**
	 * Main Page
	 * 
	 * @return
	 */
	@RequestMapping(value = "/get", method = RequestMethod.GET)
	@ResponseBody
	public List<Calendar> getSchedule(Authentication auth) {
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		List<Calendar> list = schedule.getScheduleByUser(userInfo);
		return list;
	}
	
	@RequestMapping(value = "/insert", method = RequestMethod.POST)
	public ModelAndView moveinsert(@RequestParam(name = "selectDate") String date) {
		ModelAndView mav = new ModelAndView("/views/bpschedule_insert");
		List<Code> type = schedule.getScheduleTypeList();
		mav.addObject("insertDate", date);
		mav.addObject("type", type);
		return mav;
	}
	
	@RequestMapping(value = "/detail", method = RequestMethod.POST)
	public ModelAndView detail(Authentication auth, @RequestParam(name = "calSerialNo") String calSerialNo) {
		ModelAndView mav = new ModelAndView("/views/bpschedule_detail");
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		Calendar detail = schedule.getScheduleByCalserialNo(userInfo, calSerialNo);
		
		// 날짜변환
		SimpleDateFormat sf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm"); //ISO date
		Date start = detail.getStart();
		Date end = detail.getEnd();
		
		mav.addObject("detail", detail);
		mav.addObject("start", sf.format(start));
		mav.addObject("end", sf.format(end));
		
		List<Code> type = schedule.getScheduleTypeList();
		mav.addObject("type", type);
		WeatherCode weather = schedule.getWeatherCode(detail.getWeather());
		String weatherName = weather.getEngName();
		mav.addObject("weatherName", weatherName);
		List<Map> goodsList = schedule.getRecommendGoods(detail.getBpCustomerId(), calSerialNo);
		mav.addObject("goodsList", goodsList);
		
		return mav;
	}
	
	@RequestMapping(value = "/insertSchedule", method = RequestMethod.POST)
	public ModelAndView insertSchedule(Authentication auth, @RequestParam(name = "type") String type, @RequestParam(name = "address") String address, @RequestParam(name = "stdate") String stdate, @RequestParam(name = "enddate") String enddate,
			@RequestParam(name = "title") String title, @RequestParam(name = "content") String content) {
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		
		String result = HttpConnectionUtil.connectHttpGet(weatherServer+"?"+"key=aac4958d55af4ad1a3162729180309&q=Seoul&date=" + stdate);
		
		InputSource is = new InputSource(new StringReader(result));
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(true);
        DocumentBuilder builder;
        Document doc = null;
        
        String mintemp = null;
        String maxtemp = null;
        String weatherIconUrl = null;
        String weatherCode = null;
        
        try {
			builder = factory.newDocumentBuilder();
			doc = builder.parse(is);
			XPathFactory xpathFactory = XPathFactory.newInstance();
	        XPath xpath = xpathFactory.newXPath();
	        // XPathExpression expr = xpath.compile("/response/body/items/item");
	        XPathExpression expr = xpath.compile("/data/weather");
	        NodeList nodeList = (NodeList) expr.evaluate(doc, XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                NodeList child = nodeList.item(i).getChildNodes();
                for (int j = 0; j < child.getLength(); j++) {
                    Node node = child.item(j);
                    if ("mintempC".equals(node.getNodeName())) {
                    	mintemp = node.getTextContent();
                    };
                    if ("maxtempC".equals(node.getNodeName())) {
                    	maxtemp = node.getTextContent();
                    };
                }
            }
            
            XPathExpression expr2 = xpath.compile("/data/weather/hourly");
            NodeList nodeList2 = (NodeList) expr2.evaluate(doc, XPathConstants.NODESET);
            for (int i = 0; i < nodeList2.getLength(); i++) {
                NodeList child = nodeList2.item(i).getChildNodes();
                for (int j = 0; j < child.getLength(); j++) {
                    Node node = child.item(j);
                    if ("weatherIconUrl".equals(node.getNodeName())) {
                    	weatherIconUrl = node.getTextContent();
                    };
                    if ("weatherCode".equals(node.getNodeName())) {
                    	weatherCode = node.getTextContent();
                    };
                }
            }
		} catch (ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (XPathExpressionException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
        
		logger.info(result);
		// calendar VO
		Calendar calendar = new Calendar();
		calendar.setBpCustomerId(userInfo.getId());
		calendar.setStart(new DateTime(stdate).toDate());
		calendar.setEnd(new DateTime(enddate).toDate());
		calendar.setTitle(title);
		calendar.setContents(content);
		calendar.setType(type);
		calendar.setCreateDate(new Date());
		calendar.setMintemp(mintemp);
		calendar.setMaxtemp(maxtemp);
		calendar.setWeather(weatherCode);
		calendar.setWeathericon(weatherIconUrl);
		calendar.setAddress(address);
		calendar.setRecommendCode("CD_1");
		
		schedule.insertSchedule(userInfo, calendar);
		
		HttpConnectionUtil.connectHttpGet(apiServer +"/api/RecommendClothes");
		
		ModelAndView mav = new ModelAndView("/views/bpschedule");
		return mav;
	}
	
	@RequestMapping(value = "/updateSchedule", method = RequestMethod.POST)
	public ModelAndView updateSchedule(Authentication auth, @RequestParam(name = "type") String type, @RequestParam(name = "weathericon") String weathericon, @RequestParam(name = "address") String address, @RequestParam(name = "calSerialNo") String calSerialNo, @RequestParam(name = "stdate") String stdate, @RequestParam(name = "enddate") String enddate,
			@RequestParam(name = "title") String title, @RequestParam(name = "content") String content) {
		UserInfoVO userInfo = userAuthService.getUserInfo(String.valueOf(auth.getPrincipal()));
		
		// calendar VO
		Calendar calendar = new Calendar();
		calendar.setBpCustomerId(userInfo.getId());
		calendar.setCalSerialNo(Integer.parseInt(calSerialNo));
		calendar.setStart(new DateTime(stdate).toDate());
		calendar.setEnd(new DateTime(enddate).toDate());
		calendar.setTitle(title);
		calendar.setContents(content);
		calendar.setType(type);
		calendar.setAddress(address);
		calendar.setWeathericon(weathericon);
		calendar.setUpdateDate(new Date());
		calendar.setRecommendCode("CD_1");
		
		logger.info("%%%" + title);
		
		schedule.updateSchedule(userInfo, calendar);
		
		ModelAndView mav = new ModelAndView("/views/bpschedule");
		return mav;
	}
	
	@RequestMapping(value = "/getMatchRate", method = RequestMethod.GET)
	@ResponseBody
	public String getMatchRate(String topImage, String bottomImage, String imTopCode, String imBottomCode) {
		
		String result = HttpConnectionUtil.connectHttpGet(apiServer+"/api/matchImage?imTopName="+ topImage +"&imBottomName=" + bottomImage + "&imTopCode=" + imTopCode + "&imBottomCode="+imBottomCode);
		return result;
	}

}
