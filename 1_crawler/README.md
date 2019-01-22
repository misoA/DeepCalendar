# Crawler(크롤러)

## 개요

인터넷에서 인공지능을 학습하기 위해 필요한 데이터를 모으기 위해 작성된 크롤러(Crawler)다. 이번 프로젝트에서 사용된 데이터는 미리 만들어진 데이타셋이 활용되지 않고, 직접 인터넷상에서 크롤링한 데이터를 사용하였다.

## 사용된 기술

셀레니윰을 기반으로 작성하였다. 크롤링은 chrome에서 이루어졌기에 chrome driver를 이용하였다.

1. 구글에서 query를 입력하여 나오는 image를 crawling하였다.
2. 인스타그램에서 query를 통하여 나오는 image들을 crawling 하였다.

## 작동방법 

### 구글 검색 이미지 크롤링
```
python fashion_crawler.py [keyword] [scroll]
```
- `keyword` : 구글 검색창에 검색할 키워드(query)를 입력한다. 필수 항목이다. 
- `scroll` : 스크롤을 최대 몇번 내릴지 결정한다. 숫자가 커질수록 더 많이 스크롤을 내리게 된다. 입력 안할시 default는 50으로 설정되어 있다.

#### 1. 이미지 저장 위치
사진은 현재 fashion_cralwer.py가 존재하는 폴더에 query명으로 새 폴더를 생성하고 해당 폴더에 사진을 저장하게 되어있다.

### 인스타그램 이미지 크롤링
```
python insta_crawler.py
```
명령어 동작시 별도로 입력하는 옵션은 없다.

####	1. Query 입력
코드 내부를 보면 rootUrl 변수가 있는데
`rootUrl = "https://www.instagram.com/explore/tags/가을코디룩/" `
다음과 같이 default가 설정되어 있다.
여기서 `가을코디룩`을 원하는 query로 바꿔준후 실행시켜주면 crawling을 시작한다.

####	2. 이미지 저장 위치
`insta_cralwer.py`가 위치한 path 내부의 `data/` 가 기본 path다.
이 data폴더에 이제 사진이 찍혀진 날짜별로 폴더를 만들어 그 안에 사진이 각각 저장되게 된다. 

예로 A사진은 12월 7일에 B사진이 12월 8일에 찍혔다면,
각각 A와 B사진은 서로 다른 폴더 속에 저장되게 된다.
`../data/date/img`

A - `../data/20181207/A`
B - `../data/20181208/B`

### 인스타그램 크롤링 이미지 상의 / 하의 detection

인공지능을 학습하기 위한 패션 사진으로 활용하기 위해서는 저장된 사진은 상의와 하의로 나누어야 한다. 앞서 만들어진 tensorflow detection 알고리즘을 여기에다가 사용한다. 이 파일의 종류는 두 가지로 나뉘게 된다.

#### 1. 이미지 내의 모든 상의 / 하의 이미지 세트를 crop 후 저장
```
python make_clothes_detect_img.py
```
명령어를 사용시 자동으로 상 하의를 detect후 crop하여 별도 폴더에 저장한다.

#### 2. 이미지 내의 상의  / 하의 세트 하나만 crop 후 저장
```
python make_clothes_detect_matching.py
```

#### 3. 이미지 저장 위치

사진이 저장된 곳은 `../data`
```
python make_clothes_detect_img.py
```
위의 명령어로 Detect 후 crop 된 사진이 저장되는 곳은 
`../boundingbox_img_insta`
```
python make_clothes_detect_matching.py
```
위의 명령어로 Detect 후 crop 된 사진이 저장되는 곳은
`../boundingbox_img_matching`

날짜별로 폴더를 만들어 각각 사진을 저장하는 것은 동일하다. 

예시로 A사진을 들면

`../data/20181207/A` 는 다음의 두 가지 명령에 따라 각각 폴더에 저장된다

```
python make_clothes_detect_img.py
```
`../boundingbox_img_insta/201081207/A`로 저장되게 된다.
```
python make_clothes_detect_matching.py
```
`../boundingbox_img_matching/201081207/A`로 저장되게 된다.
