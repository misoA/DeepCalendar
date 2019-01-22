# Schedule classification (일정 분류)

## 개요

옷의 이미지를 보고 옷의 일정을 알아맞히는 모델이다.

1. daily
2. date
3. party
4. school
5. speech
6. sport
7. trip
8. work

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

`C:/deepc/dataset/raw_data/schedule`

옷 종류로 daily를 생각하고 해당 이미지를 가지고 있다면 다음과 같은 폴더를 추가적으로 만든다.

`C:/deepc/dataset/raw_data/schedule/daily/`

이후에 daily 이미지들을 위의 path에 집어넣으면 된다. 만약 옷 종류를 더 늘리고 싶다면
```
C:/deepc/dataset/raw_data/schedule/daily/
C:/deepc/dataset/raw_data/schedule/date/
C:/deepc/dataset/raw_data/schedule/party/
```
등으로 폴더를 추가한후 학습용 이미지를 안에 넣어준다.
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

`C:/deepc/dataset/raw_data/clothes`의 모든 이미지를
`C:/deepc/dataset/preprocess_data/clothes`의 path로 복사하여 붙여넣는다.
이때 세부 항목을 별도로 분류하지 않고 한 폴더 안에 다 넣는다.

라벨 생성은 다음과 같다.

> `Annotation label_file data structure`
>
> [{'image': image_id(str), 'label', label(int)}]
>
> Ex: [{'image': 'im_1' 'label': 1},

각 이미지마다 dictionary를 만들어 이미지 이름과 옷 종류에 따른 숫자를 부여한다.
옷 종류에 부여되는 숫자는 해당 옷 종류가 `C:/deepc/dataset/raw_data/clothes/`에서
몇 번째 폴더에 위치하는지에 따라 결정된다. 다음과 같은 순서로 폴더가 생성되었다 가정하자.
```
C:/deepc/dataset/raw_data/schedule/daily
C:/deepc/dataset/raw_data/schedule/date
C:/deepc/dataset/raw_data/schedule/party
```

`daily`의 label은 `0`

`date`의 label은 `1`

`party`의 label은 `2` 

와 같은 형태로 이루어진다. 이런 라벨 정보들은 한 곳에 모아져 학습용과 테스트용으로 나뉘어 저장된다.

`schedule_train.json`

`schedule_test.json`

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