package com.blackpineapple.web.service;

import java.util.List;

import com.blackpineapple.dao.generate.model.BPCustomer;
import com.blackpineapple.dao.generate.model.Code;
import com.blackpineapple.web.vo.ClothesVO;

public interface DataService {

	public BPCustomer insertCustomer(String inputId, String encodePassword, String inputNickname, String inputShirt, String inputPants, String inputHeight, String inputWeight, String inputRemark);

	public List<ClothesVO> getRandomClothesList();
	
	public List<Code> getStyleCategoryCodeList();

	public boolean nicknameDuplicate(String nickname);

	public boolean idDuplicate(String id);
	
	public void insertClothesStars(String id, List<ClothesVO> clothesList, String usualStyleCode, String usualStyleName, String wantedStyleCode, String wantedStyleName);

}
