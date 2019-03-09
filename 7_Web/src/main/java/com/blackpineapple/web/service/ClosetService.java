package com.blackpineapple.web.service;

import java.util.List;
import java.util.Map;

import com.blackpineapple.dao.generate.model.Closet;
import com.blackpineapple.dao.generate.model.Code;
import com.blackpineapple.dao.generate.model.GoodsTag;
import com.blackpineapple.web.vo.UserInfoVO;

public interface ClosetService {

	public List<Map> getClosetByUser(UserInfoVO user);
	
	public Closet insertCloset(Closet Closet);

	public Object getClosetByCalserialNo(UserInfoVO user, String calSerialNo);

	void updateCloset(Closet Closet);

	void insertGoodsTag(GoodsTag GoodsTag);
	
	public Code getClothesCode(String codeName, String preCodeName);
	
	public void insertClothesCodeTag(Map<String, Object> map, int closetId);

	public List<GoodsTag> getGoodsTagList(String goodsId, String predictCode);

}
