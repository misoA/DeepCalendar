# Matching Regression (매칭 회귀)

## 개요

`상의`와 `하의` 두 이미지를 입력받았을때 **패션의 관점에서 얼마나 어울리는지를 판단하는 모델**이다.

## 폴더 / 파일 설명

>아래의 폴더 / 파일 구성은 딥러닝 모델 각각(옷 종류 / 일정 / 날씨) 에서 모두 동일하다.

`Model` - 학습된 딥러닝 모델의 weight값이 담긴 pickle폴더를 epoch별로 저장해놓는 `폴더`

`dataset` - 데이타셋을 만들기 위한 과정 중에 생성하는 중간 파일을 임시 보관하는 `폴더`

`Configure.py` - train.py와 inference.py에서 해야될 핵심적인 설정값들을 종합해놓았다.

`Data_analysis.py` - inference.py를 실행하여 나온 결과 파일을 분석한다.

`Data_generator.py` - crawler로 모아진 raw image를 처리하여 학습용 이미지를 별도의 폴더에 저장하고 label을 생성한다. 

`Data_loader.py` - 특정 이미지와 해당 이미지의 라벨 값을 돌려준다.

`Inference.py` - 학습된 딥러닝 모델의 성능을 테스트

`Model.py` - pytorch로 작성된 딥러닝 모델

`Train.py` - 딥러닝 모델을 학습하는 곳

## 작동방법 

### 1. 학습할 이미지 raw_data 폴더에 집어넣기
	
`Configure.py`에 들어가면 기본 설정이다.

```
PC = 1
path_list = ["/jet/prs/workspace/fashion-cnn", "C:"]
```
`Path_list`의 리스트 `좌측`은 aws ec2에서 설정된 path이며, `우측`은 local pc에서 설정한 기본 path다.
PC변수로 리스트 안의 path를 선택한다. 현재는 `PC=1`이므로 `C:`가 선택되어있는 상태다.
만약 `D:`폴더나 혹은 다른 path를 기본 path로 사용하고 싶다면 위의 `path_list`를 수정하면 된다.
`Path_list` 중 하나의 path를 기본 path로 지정하고 여기에 `/deepc/dataset/raw_data/`를 붙여주면
해당 path가 바로 학습용 데이터가 보관될 path다.

`C:/deepc/dataset/raw_data/`

여기에 어떤 종류의 딥러닝 모델인지 우측에 적어준다. 예시는 옷 종류 분류용 path 명이다.

`C:/deepc/dataset/raw_data/match`

얼마나 상의와 하의가 어울리는지 여부를 0부터 1까지 점수를 매겼고
각 점수를 하위 폴더명으로 만든다.
여기서는 5가지 점수로 나뉘었다 `(0 / 0.2 / 0.5 / 0.8 / 1)`

`C:/deepc/dataset/raw_data/match/0/`

옷 이미지를 해당하는 날짜 폴더 안에 각각 집어넣는다.

정리하자면 다음과 같다.

```
Path_list의 path/deepc/dataset/raw_data/딥러닝 모델 키워드/세부 항목/
```

설정한 path와 실제 컴퓨터에 이미지가 저장되어있는 path가 동일해야 한다.

### 2. 학습용 이미지가 모아진 별도 폴더 생성 및 라벨 생성
```
Python data_generator.py
```
위의 명령어 동작시 모든 것이 자동으로 이루어진다.

`C:/deepc/dataset/raw_data/match`의 모든 이미지를
`C:/deepc/dataset/preprocess_data/match`의 path로 복사하여 붙여넣는다.
이때 세부 항목을 별도로 분류하지 않고 한 폴더 안에 다 넣는다.

라벨은 `최고 온도`와 `최저 온도` 두 가지로 나누어 생성한다.
온도는 [https://www.worldweatheronline.com/](https://www.worldweatheronline.com/) 사이트에서 제공하는 API를 사용하였다.
`2018-12-03`와 같이 날짜를 입력하면 해당 날짜의 `최저 온도`와 `최고 온도`를 제공하여 준다.

> `Annotation label_file data structure`
>
> [{'image_1': image_id(str), 'image_2': image_id(str), 'label', label(int)}]
>
> Ex: [{'image_1': 'im_1', 'image_2':'im_2', 'label': 1}]

각 상하의 세트마다 dictionary를 만들어 `상의` `하의` 각 `이미지 이름`과 `점수`를 저장한다.
이런 라벨 정보들은 한 곳에 모아져 학습용과 테스트용으로 나뉘어 저장된다.

`match_train.json`

`match_test.json`

### 3. 학습

Configure.py에 들어가면 다음의 변수 두개가 존재한다.
```
train_epoch = None
inference_epoch = 30
```
`Train_epoch`는 **학습시에 앞서 학습된 모델의 weight에 이어서 학습하고 싶을 시 사용**한다.
`None`은 처음부터 학습한다는 의미이며, `10`으로 입력시 `10 epoch 학습`을 통해 나온 모델의
Weight를 불러와서 이어서 학습하겠다는 의미이다.

`Inference_epoch`는 **몇 epoch만큼 학습된 모델의 weight로 테스트하고 싶은지 결정하는 수치**다.
`30`이 **default 설정**이며 이는 `30 epoch 학습된 모델의 weight를 학습`하겠다는 의미이다. 

이후 `TEM`변수를 설정해준다. 
이는 **최고 온도와 최저 온도 어떤 온도를 기준으로 학습할지 정하는 변수**다.

`TEM = 0` **옷의 최고 온도**

`TEM = 1` **옷의 최저 온도**

이를 설정한 후, `train.py` 파일로 들어가서 하이퍼파라메타를 설정한다.
```
batch_size = 50
num_epochs = 30
save_every = 1
print_every = 10
log_file = 'training_log.txt'
optimizer = optim.Adam(params, lr=0.001)
```
배치 크기를 설정하고, `num_epoch`에서 최대 몇번 학습할지 정한다.
`Save_every`는 **몇 epoch마다 저장할지 정하는 변수**다.
`Print_every`는 **몇 batch마다 결과를 standard output으로 내보낼지 정하는 변수**다.
현재 `optimizer`는 `adam`으로 사용중이며 `lr`에서 `learning rate`를 조정할 수 있다.

위 사항이 모두 조정되었으면 다음의 명령어를 실행한다.
```
Python train.py
```
### 4. 테스트

`Inference.py` 파일의 `batch_size`만 수정 후 다음의 명령어를 실행한다.
```
Python test.py
```
모든 과정이 끝났다. 결과가 만족스럽다면 학습된 weight를 사용하면 된다.
최종적으로 최고온도용 모델의 weight와 최저 온도용 weight 두 가지가 나오게 된다.