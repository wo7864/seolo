# Celligrapick
GAN을 활용한 손글씨 생성 프로젝트입니다.
현재는 프로토 타입으로, 영어 손글씨를 생성할 수 있습니다.
최종적으로는 한글 캘리그라피를 생성하는 것을 목표로 합니다.

![UI](/others/UI.PNG)

## Intro
- Install
  - Server
  - Client
- Data Set
- Model Create
- Select Model
- Load Model & Generate Image
- Development Environment
- reference

## Install
- Server

	0. install python3
	1. git clone https://git.swmgit.org/root/p1017_dblock.git
	2. 가상환경 실행(venv)
	3. python 라이브러리 설치(pip install django djangorestframework opencv-python tensorflow matplotlib keras)
	4. python manage.py runserver
- Client

	0. install nodejs(npm)
	1. npm install --save react react-dom react-script
	2. frontend/src/app.js내부 axios.post(url) 본인 서버로 수정
	3. npm start



## Data set - Kaggle - A-Z Handwritten Alphabets in .csv format

![DataSet](/others/dataset.png)

https://www.kaggle.com/sachinpatel21/az-handwritten-alphabets-in-csv-format


### Model Create
모델 생성은 ipynb 파일로 작성되어 Google Colab, 또는 Jupyter notebook 환경에서 진행합니다.

1. open **automation_keras_gan_alphabet.ipynb**
2. 2번째 셀의 data_dir의 경로를 본인의 경로로 경로를 수정합니다.
3. 9번째 셀의 Model Class 내부의 fit 함수에서 save_dir을 본인의 경로로 수정합니다. 
4. 1~9셀을 실행시켜 모델을 생성합니다.

**save_dir 내에 여러 폴더들이 미리 생성되어 있어야합니다.**

**학습에 실패한 모델은 아무것도 생성하지 않습니다. 재학습이 필요합니다**

### Select Model
save_dir 내의 img, model, z_value 디렉토리에는 각 모델, 생성할 수 있는 이미지, 그에 대응되는 input vector가 저장됩니다.
img 폴더 내에서 각 알파벳 별로 가장 변화가 다양하고 뚜렷한 이미지를 선택합니다.

ex) G_450.png 일 경우, model, z_value 디렉토리에서 G_450.h5, G_450.json, G_450_.txt를 모두 선택합니다.

![generated img](/others/G_450.png)

해당 이미지에서 가장 다른 특성을 지닌 4개의 그림을 선택하고 alphabet_parameter.csv 파일을 작성합니다.

### Load Model & Generate Image

1. keras_load_model.py > main에서 호출 된 excute 함수의 인자 변경
2. keras_load_model.py 실행
**model, z_value, result 디렉토리의 경로를 본인에 맞게 설정해 주어야합니다.**


## Development Environment
- Google Colab
- Windows 10
- Python3, Javascript

## reference
- https://www.kaggle.com/sachinpatel21/az-handwritten-alphabets-in-csv-format
- http://jaejunyoo.blogspot.com/2017/02/deep-convolutional-gan-dcgan-1.html
- https://github.com/mattya/chainer-DCGAN
- https://neurowhai.tistory.com/153
- https://arxiv.org/abs/1511.06434
...추가 예정

### other
소프트웨어 마에스트로 10기 컴코딩(Comcoding)팀 프로젝트입니다.

