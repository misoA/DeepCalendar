package com.blackpineapple.web.vo;

import org.springframework.context.annotation.PropertySource;

import lombok.Data;

@Data
@PropertySource("classpath:config/properties/web.ALL.properties")
public class UserInfoVO {

	private String	id;

	private int		roleId;

	private String	name;
	
}
