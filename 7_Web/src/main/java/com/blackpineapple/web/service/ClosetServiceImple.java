/**
 * Created Date : 2016. 9. 5. 오전 11:13:15
 * Copyright©2002 Nbware All rights reserved.
 * 
 * @author Miso
 */
package com.blackpineapple.web.service;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.ibatis.session.SqlSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.SessionAttributes;

import com.blackpineapple.dao.generate.mapper.ClosetMapper;
import com.blackpineapple.dao.generate.mapper.CodeMapper;
import com.blackpineapple.dao.generate.mapper.GoodsTagMapper;
import com.blackpineapple.dao.generate.model.Closet;
import com.blackpineapple.dao.generate.model.ClosetExample;
import com.blackpineapple.dao.generate.model.Code;
import com.blackpineapple.dao.generate.model.CodeExample;
import com.blackpineapple.dao.generate.model.ClosetExample.Criteria;
import com.blackpineapple.dao.generate.model.GoodsTag;
import com.blackpineapple.dao.generate.model.GoodsTagExample;
import com.blackpineapple.web.controller.ClosetController;
import com.blackpineapple.web.vo.UserInfoVO;

@SessionAttributes("user")
@Service("Closet")
public class ClosetServiceImple implements ClosetService {
	@Autowired
	private ClosetMapper	calMapper;
	
	@Autowired
	private GoodsTagMapper  goodsMapper;

	@Autowired
	private CodeMapper codeMapper;

	@Autowired
	private SqlSession sqlSessionTemplate;
	
	@Override
	public List<Map> getClosetByUser(UserInfoVO user) {
		
		Map paramMap = new HashMap<>();
		paramMap.put("bpCustomerId", user.getId());
		
		return sqlSessionTemplate.selectList("custom.getClosetByUser", paramMap);
	}

	@Override
	public Closet insertCloset(Closet closet) {
		
		calMapper.insert(closet);
		return closet;
		
	}
	
	@Override
	public void insertGoodsTag(GoodsTag GoodsTag) {
		
		goodsMapper.insert(GoodsTag);
		
	}
	
	@Override
	public void updateCloset(Closet Closet) {
		
		calMapper.updateByPrimaryKey(Closet);
		
	}
	
	@Override
	public void insertClothesCodeTag(Map<String, Object> map, int closetId) {
		
		for (Map.Entry<String, Object> en : map.entrySet()) {
			
			String keyName = en.getKey();
			if (!"temperature".equals(keyName)) {
				Map<String, Object> m = (Map<String, Object>) en.getValue();
				Map<String, Object> total = (Map<String, Object>) m.get("total");
				String predict = (String) m.get("predict");
				
				
				for (Map.Entry<String, Object> enn : total.entrySet()) {
					GoodsTag goodsTag = new GoodsTag();
					Code code = this.getClothesCode(enn.getKey(), keyName);
					goodsTag.setMalCf1Code("PV_1");
					goodsTag.setPredictCode(code.getCodeId());
					goodsTag.setPredictParentsCode(code.getPreCodeId());
					goodsTag.setPrdictRate((Double)enn.getValue());
					goodsTag.setGoodsId(closetId);
					goodsTag.setCreateDate(new Date());
					if (predict.equals(enn.getKey())) {
						goodsTag.setBestYn("Y");
					} else {
						goodsTag.setBestYn("N");
					}
					
					this.insertGoodsTag(goodsTag);
				}
			} else {
				
				Map<String, Object> m = (Map<String, Object>) en.getValue();
				
				for (Map.Entry<String, Object> enn : m.entrySet()) {
					GoodsTag goodsTag = new GoodsTag();
					Code code = this.getClothesCode(enn.getKey(), keyName);
					goodsTag.setMalCf1Code("PV_1");
					goodsTag.setPredictCode(code.getCodeId());
					goodsTag.setPredictParentsCode(code.getPreCodeId());
					goodsTag.setPrdictRate((Double) enn.getValue());
					goodsTag.setGoodsId(closetId);
					goodsTag.setCreateDate(new Date());
					
					this.insertGoodsTag(goodsTag);
				}
				
			}
			
			
		}
		
	}
	
	@Override
	public Closet getClosetByCalserialNo(UserInfoVO user, String calSerialNo) {
		
		ClosetExample cal = new ClosetExample();
		Criteria criteria = cal.createCriteria();
		criteria.andBpCustomerIdEqualTo(user.getId());
		List<Closet> calList = calMapper.selectByExample(cal);
		
		return calList.get(0);
	}
	
	@Override
	public Code getClothesCode(String codeName, String preCodeName) {
		
		CodeExample code = new CodeExample();
		code.createCriteria().andCodeNameEqualTo(codeName).andPreCodeNameEqualTo(preCodeName);
		List<Code> codeList = codeMapper.selectByExample(code);
		
		return codeList.get(0);
		
	}
	
	@Override
	public List<GoodsTag> getGoodsTagList(String goodsId, String predictCode) {
		
		GoodsTagExample cal = new GoodsTagExample();
		cal.createCriteria().andGoodsIdEqualTo(Integer.parseInt(goodsId)).andPredictCodeEqualTo(predictCode);
		List<GoodsTag> calList = goodsMapper.selectByExample(cal);
		
		return calList;
	}

}
