# Deep Calendar Web

## Web 환경
- `SpringFramework with Maven` 기반 웹서버 구축
- `MyBatis`
- `Hibernate`
- `fullcalendar` javascript 기반 달력 플러그인

## Workflow

### 회원가입, 로그인

- 회원가입 시 사용자의 취향을 취합한다.(이 데이터는 의상 추천시 활용됨)
- 로그인은 `spring security`를 사용하였다.

### 옷장

본인이 소유한 옷을 등록 및 관리한다. 
추천시 옷장의 옷을 분석하여 추천하게 된다.
    1. 옷 등록시 detection을 사용하여 상의, 하의로 분리하여 사용자에게 제공
    2. 사용자가 본인이 등록할 의상을 선택한다.  
    3. 의상 선택후 의상의 카테고리와 이름을 입력하고 저장한다.

### 일정
fullcalendar 플러그인을 사용한 달력화면을 사용하며 일정의 등록, 확인, 수정한다.  
    1. 일정을 등록하고 싶은 날짜를 클릭하면 일정 등록화면 이동.
    2. 추천을 받을 이벤트 특성(파티, 여행) 등을 선택하여 등록.
    3. 일정을 등록하면 해당날짜에 일정이 표시되며 클릭시 상세 내용을 확인할 수 있고 추천된 의상을 볼 수 있다.

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
