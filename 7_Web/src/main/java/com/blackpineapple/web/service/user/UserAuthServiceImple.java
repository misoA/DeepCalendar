/**
 * Created Date : 2016. 9. 5. 오전 11:13:15
 * Copyright©2002 Nbware All rights reserved.
 * 
 * @author Miso
 */
package com.blackpineapple.web.service.user;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.collections4.CollectionUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.blackpineapple.dao.generate.mapper.BPCustomerMapper;
import com.blackpineapple.dao.generate.mapper.BPRoleMapper;
import com.blackpineapple.dao.generate.model.BPCustomer;
import com.blackpineapple.dao.generate.model.BPCustomerExample;
import com.blackpineapple.web.vo.UserInfoVO;

/**
 * 
 * @author MIS
 *
 */
@Service("userAuthService")
public class UserAuthServiceImple implements UserDetailsService {

	private static final Logger	log	= LoggerFactory.getLogger(UserAuthServiceImple.class);

	@Autowired
	private BPCustomerMapper		userMapper;

	@Autowired
	private BPRoleMapper		roleMapper;

	@Override
	public UserDetails loadUserByUsername(String id) throws UsernameNotFoundException {

		UserDetails user;

		log.info("Login id Setting = " + id);
//		BPAdminExample userEx = new BPAdminExample();
		BPCustomerExample userEx = new BPCustomerExample();
		userEx.createCriteria().andBpCustomerIdEqualTo(id);
		List<BPCustomer> userInfoList = userMapper.selectByExample(userEx);
		log.info("Login userInfoList = " + userInfoList);
		if (CollectionUtils.isNotEmpty(userInfoList)) {
			BPCustomer userInfo = userInfoList.get(0);
			log.info("Login User Setting = " + userInfo.toString());
			// 리턴할 권한 정보
			ArrayList<SimpleGrantedAuthority> returnRoles = new ArrayList<SimpleGrantedAuthority>();
//			 리턴할 권한 정보 세팅
//			returnRoles.add(new SimpleGrantedAuthority(roleMapper.selectByPrimaryKey(userInfo.getBpCustomerPassword().getRoleName()));
			// 로그인 정보 리턴
			user = new User(id, userInfo.getBpCustomerPassword(), returnRoles);
		} else {
			throw new UsernameNotFoundException("해당 유저가 없습니다");
		}
		return user;
	}

	public UserInfoVO getUserInfo(String id) {
		UserInfoVO user = new UserInfoVO();

		BPCustomerExample userEx = new BPCustomerExample();
		userEx .createCriteria().andBpCustomerIdEqualTo(id);
		List<BPCustomer> userInfoList = userMapper.selectByExample(userEx);

		if (CollectionUtils.isNotEmpty(userInfoList)) {
			BPCustomer bPCustomer = userInfoList.get(0);
			user.setId(bPCustomer.getBpCustomerId());
			user.setName(bPCustomer.getBpCustomerNickname());
//			user.setRoleId(bPCustomer.getAdminRoleId());
		} else {
			throw new UsernameNotFoundException("해당 유저가 없습니다");
		}

		return user;
	}

}
