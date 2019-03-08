package com.blackpineapple.web.vo;

import lombok.Data;

@Data
public class recommendVO implements Comparable<recommendVO>{

	private int		clothesId;
	private double	clothesRank;
	private String	clothesName;
	private String	clothesImageUrl;
	private String	shopLinkUrl;
	private int	price;
	
	
	
	@Override
	public int compareTo(recommendVO o) {
		if (o.clothesRank > this.clothesRank) {
			return 1;
		} else {
			return -1;
		}
	}



	public recommendVO(int clothesId, double clothesRank, String clothesName, String clothesImageUrl, String shopLinkUrl, int price) {
		super();
		this.clothesId = clothesId;
		this.clothesRank = clothesRank;
		this.clothesName = clothesName;
		this.clothesImageUrl = clothesImageUrl;
		this.shopLinkUrl = shopLinkUrl;
		this.price = price;
	}



	public recommendVO() {
		super();
		// TODO Auto-generated constructor stub
	}
	
	

}