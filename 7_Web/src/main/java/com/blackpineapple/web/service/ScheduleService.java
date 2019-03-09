package com.blackpineapple.web.service;

import java.util.List;
import java.util.Map;

import com.blackpineapple.dao.generate.model.Calendar;
import com.blackpineapple.dao.generate.model.Code;
import com.blackpineapple.dao.generate.model.WeatherCode;
import com.blackpineapple.web.vo.UserInfoVO;

public interface ScheduleService {

	public List<Calendar> getScheduleByUser(UserInfoVO user);
	
	public void insertSchedule(UserInfoVO user, Calendar calendar);

	public Object getScheduleByCalserialNo(UserInfoVO user, String calSerialNo);

	public void updateSchedule(UserInfoVO user, Calendar calendar);

	public List<Code> getScheduleTypeList();

	public WeatherCode getWeatherCode(String weatherCodeId);

	public List<Map> getRecommendGoods(String bpCustomerId, String calSerialNo);

}
