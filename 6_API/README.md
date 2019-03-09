# Deep Calendar API

##### Python Flask 기반의 API 서버

## API List
- `S3download('fromfile', 'tofilename')` : Image 서버의 자원을 로컬로 다운로드
- `detectImage('detectImName')` : 이미지 Detection 및 crop 하여 Image 서버에 저장 후 URL 반환
- `ClassificateImage('imName')` : 이미지를 의상 카테고리/일정 카테고리/날씨/온도에 따라 분류하여 태그 반환
- `RecommendClothes` : 추천 필요 일정을 확인 후, 일정별 추천 의상 매핑 
- `matchImage('imTopName','imBottomName','imTopCode','imBottomCode')` : 상의와 하의를 입력하여 매칭률을 반환
  
## API 서버 구조
`run.py` : API 서버 설정

`config.py` : DB 설정

`migrate.py` : DB Model 읽어오기 설정

`Model.py` : Model 정의

`app.py` : API URI 및 resource 정의 

## 사용 방법
- http 기반의 get/post 호출을 이용하여 API 서버 호출
- DB 및 Image 서버 구축 필요

`API 별 학습 방법` : 상위 1~5 폴더 내용 참조

`API의 사용 코드` : [상위 7_Web 폴더](https://github.com/misoA/DeepCalendar/tree/master/7_Web) 참조  

