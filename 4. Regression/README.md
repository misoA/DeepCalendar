# 깊은 달력 (a.k.a. Deep Calendar)

##### 사용자의 일정과 취향을 고려하여, 옷을 추천해주는 깊고 멋진 서비스

**주의** 
_소스코드 업로드와 readme 수정을 진행중입니다
완성본이 아닙니다_


![main page](./main.jpg)

## 왜 만들었나요?
사람들은 매일 아침 오늘 뭐입지? 에 대한 고민을 합니다.
특히 소개팅, 결혼식, 미팅 등 중요한 일정이 있을 땐, 고민의 강도가 더 심해집니다.
가족 혹은 친구에게 패션을 조언 받기도 하겠지만, 매일 조언을 얻는 것은 서로에게 매우 피곤한 일입니다.

**깊은 달력**은 일정을 기반으로 해당 일정에 어울리는 패션을 추천합니다.
사용자는 자신의 취향을 입력하고 일정을 등록하면 매일 아침 오늘에 어울리는 패션을 추천받을 수 있습니다.



## 프로젝트 구성요소

##### 1. Crawler
##### 2. Detection
> 크롤러에서 수집한 이미지에서 상의(top)/하의(bottom)를 Object Detection(tensorflow-Faster RCNN), 잘라낸 이미지를 저장하여 이후 과정 학습에 사용함.
> (ref : https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)
##### 3. Classification
##### 4. Regression
##### 5. Recommendation
> 고객의 일정/취향에 맞는 의상을 추천함 (User-based Collaboration-Filltering)  
> 1. 고객의 일정 특성에 따라 의상을 필터링
> 2. 의상별 사용자별 별점을 이용하여 사용자들의 취향 유사도를 계산함
> 3. 유사도가 가장 높은 다른 사용자가 별점을 높게 준 의상을 추천함
##### 6. API (Python Flask 기반의 API 서버)
> [API List]
> 1. S3download('fromfile', 'tofilename') : Image 서버의 자원을 로컬로 다운로드
> 2. detectImage('detectImName') : 이미지 Detection 및 crop 하여 Image 서버에 저장 후 URL 반환
> 3. ClassificateImage('imName') : 이미지를 의상 카테고리/일정 카테고리/날씨/온도에 따라 분류하여 태그 반환
> 4. RecommendClothes : 추천 필요 일정을 확인 후, 일정별 추천 의상 매핑 
> 5. matchImage('imTopName','imBottomName','imTopCode','imBottomCode') : 상의와 하의를 입력하여 매칭률을 반환
##### 7. Web
##### 8. DB
##### 9. Image Server
> AWS S3를 이용하여 Static Image 서버 구축(https 이미지 호스팅)
> AWS CLI를 각 서버에서 접근



## 어떻게 쓰나요?
지금 당장은 사용하실 수 없습니다.
BUT, **★ STAR**를 클릭 하신 후 **깊은 달력** github를 clone or download 하여 아래의 튜토리얼을 따라오신다면
여러분은 충분히 멋지고 깊은 달력을 사용하실 수 있습니다





## Appendix

### 깊은 달력의 인공지능
깊은 달력은 Python 기반의 기본적인 인공지능 기술들을 학습시켰습니다.

깊은 달력은 다음과 같은 흐름으로 동작합니다.
1. 사용자는 자신의 취향을 등록합니다.
2. 그리고 자신의 옷장에 있는 옷을 사진으로 등록합니다.
3. 사진에서 상/하의가 있는 부분을 찾아내서 각각 따로 저장합니다. (Object Detection)
4. 상/하의의 특성을 태깅합니다. (Classification: 일정/온도/날씨/옷카테고리)
5. 사용자가 일정을 등록합니다.
6. 사용자의 옷에 일정에 적합한 지에 대한 점수를 부여합니다.
7. 일정마다 옷에 점수가 상이하게 매겨집니다.
8. 일정별로 높은 점수를 부여받은 옷에 한하여 사용자의 취향에 적합한지 분석하여 가장 적합한 옷을 선택합니다.
9. 일정별로 선택된 상하의 옷을 기반으로 가장 어울리는 상하의 조합을 찾아냅니다.
10. 최종적으로 선택된 상하의 세트 3개를 추천합니다.

1. 추천 알고리즘에 의해 해당 유저의 취향 옷 1차 선별
2. 선별된 옷 중 유저가 입력한 일정 정보에 적합한 옷 2차 선별
3. 2차 선별을 통과한 옷 중에서 가장 어울리는 상의 하의 조합을 찾아내어서 추천


**Tagging**
Reference : https://github.com/IllgamhoDuck/CVND/tree/master/%40PROJECT%20%5BImage%20Captioning%5D
1. 옷 카테고리
2. 날씨
3. 일정별
4. 온도
5



## License
![main page](./bplogo.jpg)

