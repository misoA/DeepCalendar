# Deep Calendar Recommendation

고객의 `일정`, `취향`에 맞는 의상을 추천함 (User-based Collaboration-Filltering)  
 1. 고객의 일정 특성에 따라 의상을 필터링
 2. 의상별 사용자별 별점을 이용하여 사용자들의 취향 유사도를 계산함
 3. 유사도가 가장 높은 다른 사용자가 별점을 높게 준 의상을 추천함
  
## Recommendation 사용 기술
Scikit Learn의 cosine_similarity를 이용하여 collaboration filtering을 구현함

1. 추천을 진행할 고객 리스트 저장
2. 고객별 옷장 상품 리스트 저장
3. 고객별 옷장 상품을 일정 특성별(날씨, 카테고리, 온도 가중치)로 필터링
4. 추천을 진행할 고객과 유사한(신체사이즈 유사, 취향 유사) 고객 리스트 저장
5. 유사 고객에 대하여 2,3과정 진행
6. 고객 배열 생성 후 유사도 검증 (null 값의 경우 평균 저장)
    ```
    consine_similarity = consine_similarity(유사고객,신규고객)


    유사도 점수 = 유사고객 점수배열 * consine_similarity
    ```
7. 유사도 높은 순서대로 상품 추천

## 사용 방법

추천을 진행하기 전, 이미지에 대한 [Detection](https://github.com/misoA/DeepCalendar/tree/master/2_detection)과 [Classification](https://github.com/misoA/DeepCalendar/tree/master/3_classification)/[Regression](https://github.com/misoA/DeepCalendar/tree/master/4_Regression)에 따른 Tagging이 선행되어야 함

소스코드 : https://github.com/misoA/DeepCalendar/blob/master/6_API/resources/CollaborationFiltering.py 참조

