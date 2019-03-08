package com.blackpineapple.web.service;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;

import org.apache.commons.collections4.CollectionUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.blackpineapple.dao.generate.mapper.BPCustomerMapper;
import com.blackpineapple.dao.generate.mapper.BPRatingMapper;
import com.blackpineapple.dao.generate.mapper.BrandMapper;
import com.blackpineapple.dao.generate.mapper.CodeMapper;
import com.blackpineapple.dao.generate.mapper.MusinsaGoodsMapper;
import com.blackpineapple.dao.generate.mapper.MusinsaReviewMapper;
import com.blackpineapple.dao.generate.mapper.SsmkGoodsMapper;
import com.blackpineapple.dao.generate.model.BPCustomer;
import com.blackpineapple.dao.generate.model.BPCustomerExample;
import com.blackpineapple.dao.generate.model.BPRating;
import com.blackpineapple.dao.generate.model.Code;
import com.blackpineapple.dao.generate.model.CodeExample;
import com.blackpineapple.dao.generate.model.MusinsaGoods;
import com.blackpineapple.dao.generate.model.MusinsaGoodsExample;
import com.blackpineapple.dao.generate.model.SsmkGoods;
import com.blackpineapple.dao.generate.model.SsmkGoodsExample;
import com.blackpineapple.web.vo.ClothesVO;

@Service
public class DataServiceImple implements DataService {

	private static final Logger	logger	= LoggerFactory.getLogger(DataServiceImple.class);

	@Autowired
	private BPCustomerMapper	bPCustomerMapper;

	@Autowired
	private BPRatingMapper		bpRatingMapper;

	@Autowired
	private MusinsaGoodsMapper	musinsaGoodsMapper;

	@Autowired
	private SsmkGoodsMapper		ssmkGoodsMapper;

	@Autowired
	private CodeMapper			codeMapper;

	@Override
	public BPCustomer insertCustomer(String inputId, String encodePassword, String inputNickname, String inputShirt, String inputPants, String inputHeight, String inputWeight,
					String inputRemark) {

		BPCustomer customer = new BPCustomer();
		customer.setBpCustomerId(inputId);
		customer.setBpCustomerPassword(encodePassword);
		customer.setBpCustomerNickname(inputNickname);
		customer.setShirtSize(inputShirt);
		customer.setPantsSize(inputPants);
		customer.setBpCustomerHeight(Integer.parseInt(inputHeight));
		customer.setBpCustomerWeight(Integer.parseInt(inputWeight));
		customer.setRemark(inputRemark);
		customer.setCreateDate(new Date(Calendar.getInstance(Locale.KOREA).getTimeInMillis()));
		bPCustomerMapper.insert(customer);

		return customer;
	}

	@Override
	public List<ClothesVO> getRandomClothesList() {

		List<ClothesVO> returnList = new ArrayList<>();

		MusinsaGoodsExample mGoodsEx = new MusinsaGoodsExample();
		mGoodsEx.createCriteria();
		mGoodsEx.setOrderByClause("rand() limit 15");
		List<MusinsaGoods> mGoodsList = musinsaGoodsMapper.selectByExample(mGoodsEx);
		for (MusinsaGoods musinsaGoods : mGoodsList) {
			returnList.add(new ClothesVO(musinsaGoods));
		}

		SsmkGoodsExample sGoodsEx = new SsmkGoodsExample();
		sGoodsEx.createCriteria().andIsUseEqualTo("Y");
		sGoodsEx.setOrderByClause("rand() limit 15");
		List<SsmkGoods> sGoodsList = ssmkGoodsMapper.selectByExample(sGoodsEx);
		for (SsmkGoods ssmkGoods : sGoodsList) {
			returnList.add(new ClothesVO(ssmkGoods));
		}

		Collections.shuffle(returnList);
		return returnList;
	}

	@Override
	public boolean nicknameDuplicate(String nickname) {
		BPCustomerExample cusEx = new BPCustomerExample();
		cusEx.createCriteria().andBpCustomerNicknameEqualTo(nickname);
		long countByExample = bPCustomerMapper.countByExample(cusEx);
		if (countByExample > 0) {
			return true;
		} else {
			return false;
		}
	}

	@Override
	public boolean idDuplicate(String id) {
		BPCustomerExample cusEx = new BPCustomerExample();
		cusEx.createCriteria().andBpCustomerIdEqualTo(id);
		long countByExample = bPCustomerMapper.countByExample(cusEx);
		if (countByExample > 0) {
			return true;
		} else {
			return false;
		}
	}

	@Override
	public List<Code> getStyleCategoryCodeList() {
		CodeExample codeEx = new CodeExample();
		codeEx.createCriteria().andPreCodeIdEqualTo("ST");
		List<Code> seletedCodeList = codeMapper.selectByExample(codeEx);
		return seletedCodeList;
	}

	@Override
	public void insertClothesStars(String id, List<ClothesVO> clothesList, String usualStyleCode, String usualStyleName, String wantedStyleCode, String wantedStyleName) {
		// customer update
		BPCustomer record = new BPCustomer();
		record.setBpCustomerId(id);
		record.setMainStyleCode(usualStyleCode);
		record.setMainStyleCodeName(usualStyleName);
		record.setWantedStyleCode(wantedStyleCode);
		record.setWantedStyleCodeName(wantedStyleName);
		record.setUpdateDate(new Date(Calendar.getInstance(Locale.KOREA).getTimeInMillis()));
		bPCustomerMapper.updateByPrimaryKeySelective(record);

		// rating insert
		for (ClothesVO clothesVO : clothesList) {
			BPRating bpRating = new BPRating();
			bpRating.setBpCustomerId(id);
			bpRating.setGoodsId(String.valueOf(clothesVO.getGoodsId()));
			bpRating.setBpReviewStars(clothesVO.getRating());
			bpRating.setMalCf1Code(clothesVO.getMalCf1Code());
			bpRating.setMalCf1Name(clothesVO.getMalCf1Name());
			bpRating.setRecommendCoditionCode("CD_1");
			bpRating.setRecommendCoditionCodeName("proceeding");
			bpRating.setCreateDate(new Date(Calendar.getInstance(Locale.KOREA).getTimeInMillis()));
			bpRatingMapper.insert(bpRating);
		}
	}
}
