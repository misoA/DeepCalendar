# Deep Calendar Web

## 사용기술
SpringFramework with Maven 기반 웹서버 구축
MyBatis, Hibernate 

## Workflow
 1. 사용자 등록, 로그인
 2. 옷장 본인이 소유한 옷 등록 (등록시 사진을 분석하여 옷을 분석하여 상,하의 사진을 분리함)
 3. 캘린더 추천을 받을 일정을 해당하는 이벤트 특성(파티, 여행) 등을 선택하여 등록
 4. 등록 후 API 서버에서 분석하여 추천 의상이 등록되며 일정 상세에서 확인가능

## Tutorial

### Spring with Maven 사용 가이드
https://spring.io/guides/gs/maven/ 

### Spring 설정파일 경로 
/BpCalendar/src/main/resources/config/spring
  1. context-database.xml 데이터베이스 설정
  2. context-root.xml 컨트롤러 설정
  3. context-security.xml spring security 설정
  
### properties 경로 
/BpCalendar/src/main/resources/config/properties/web.ALL.properties
DB 커넥션, AWS S3 설정

## License
![main page](../bplogo.jpg)
