/**
 * Created Date : 2016. 9. 5. 오전 11:13:15
 * Copyright©2002 Nbware All rights reserved.
 * 
 * @author Miso
 */
package com.blackpineapple.web.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.SessionAttributes;

import com.blackpineapple.dao.generate.mapper.CalendarMapper;
import com.blackpineapple.dao.generate.mapper.CodeMapper;
import com.blackpineapple.dao.generate.mapper.WeatherCodeMapper;
import com.blackpineapple.dao.generate.model.Calendar;
import com.blackpineapple.dao.generate.model.CalendarExample;
import com.blackpineapple.dao.generate.model.CalendarExample.Criteria;
import com.blackpineapple.dao.generate.model.Code;
import com.blackpineapple.dao.generate.model.CodeExample;
import com.blackpineapple.dao.generate.model.WeatherCode;
import com.blackpineapple.dao.generate.model.WeatherCodeExample;
import com.blackpineapple.web.vo.UserInfoVO;

@SessionAttributes("user")
@Service("schedule")
public class ScheduleServiceImple implements ScheduleService {
	
	@Autowired
	private CalendarMapper	calMapper;
	
	@Autowired
	private CodeMapper codeMapper;
	
	@Autowired
	private WeatherCodeMapper weatherMapper;
	
	@Autowired
	private SqlSession sqlSessionTemplate;

	@Override
	public List<Calendar> getScheduleByUser(UserInfoVO user) {
		
		CalendarExample cal = new CalendarExample();
		cal.createCriteria().andBpCustomerIdEqualTo(user.getId());
		List<Calendar> calList = calMapper.selectByExample(cal);
		return calList;
	}

	@Override
	public void insertSchedule(UserInfoVO user, Calendar calendar) {
		
		calMapper.insert(calendar);
		
	}
	
	@Override
	public void updateSchedule(UserInfoVO user, Calendar calendar) {
		
		calMapper.updateByPrimaryKeySelective(calendar);
		
	}
	
	@Override
	public Calendar getScheduleByCalserialNo(UserInfoVO user, String calSerialNo) {
		
		CalendarExample cal = new CalendarExample();
		Criteria criteria = cal.createCriteria();
		criteria.andBpCustomerIdEqualTo(user.getId());
		criteria.andCalSerialNoEqualTo(Integer.parseInt(calSerialNo));
		List<Calendar> calList = calMapper.selectByExample(cal);
		
		return calList.get(0);
	}
	
	@Override
	public List<Code> getScheduleTypeList() {
		
		CodeExample code = new CodeExample();
		code.createCriteria().andPreCodeIdEqualTo("PR_3");
		List<Code> codeList = codeMapper.selectByExample(code);
		
		return codeList;
	}
	
	@Override
	public WeatherCode getWeatherCode(String weatherCodeId) {
		
		WeatherCodeExample wea = new WeatherCodeExample();
		wea.createCriteria().andWeatherCodeIdEqualTo(Integer.parseInt(weatherCodeId));
		List<WeatherCode> weaList = weatherMapper.selectByExample(wea);
		
		return weaList.get(0);
	}
	
	@Override
	public List<Map> getRecommendGoods(String bpCustomerId, String calSerialNo) {
		
		Map paramMap = new HashMap<>();
		paramMap.put("bpCustomerId", bpCustomerId);
		paramMap.put("calSerialNo", calSerialNo);
		
		return sqlSessionTemplate.selectList("custom.getRecommendGoods", paramMap);
	}

}
