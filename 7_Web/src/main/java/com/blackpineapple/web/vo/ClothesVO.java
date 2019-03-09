package com.blackpineapple.web.vo;

import com.blackpineapple.dao.generate.model.MusinsaGoods;
import com.blackpineapple.dao.generate.model.SsmkGoods;

import lombok.Data;

@Data
public class ClothesVO {

	private int		goodsId;

	private String	goodsName;

	private String	goodsImage;

	private String	malCf1Code;

	private String	malCf1Name;
	
	private int rating;
	
	public ClothesVO() {
		super();
	}

	public ClothesVO(MusinsaGoods mGoods) {
		super();
		this.goodsId = mGoods.getMusinsaGoodsId();
		this.goodsName = mGoods.getMusinsaGoodsName();
		this.goodsImage = mGoods.getMusinsaGoodsImg();

	}

	public ClothesVO(SsmkGoods sGoods) {
		super();
		this.goodsId = sGoods.getSsmkGoodsId();
		this.goodsName = sGoods.getSsmkGoodsName();
		this.goodsImage = sGoods.getSsmkGoodsThumbnailImg();

	}

	public ClothesVO(int goodsId, String malCf1Code, String malCf1Name) {
		super();
		this.goodsId = goodsId;
		this.malCf1Code = malCf1Code;
		this.malCf1Name = malCf1Name;
	}

}
