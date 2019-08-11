from keras.models import model_from_json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from random import *
import csv

def load_z(target):
    with open("./z_value/{}.txt".format(target), "r") as f:
        z_value = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
        z_value = z_value[1:-1].split(" ")
        z_value = [float(f) for f in z_value]
        z_value = np.array(z_value).reshape(100, 100)
    return z_value

def load_model(target):
    json_file = open("./model/{}/{}.json".format(target,target), "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("./model/{}/{}.h5".format(target, target))
    return loaded_model

def plot(samples):
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(10, 10)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28, 28), cmap='Greys_r')
    plt.tight_layout()

    return fig

def img_attach(samples, attach=20):
    img_size = 28
    width = attach*(len(samples)-1)+img_size
    result = np.zeros((img_size, width))
    result.fill(0)
    for idx, img in enumerate(samples):
        img = img.reshape(img_size, img_size)
        if idx==0:
            result[:,:img_size] = img
        else:
            for idx_i, val_i in enumerate(img):
                for idx_j, val_j in enumerate(val_i):
                    if img[idx_i, idx_j] > result[idx_i, attach*idx + idx_j]:
                        result[idx_i, attach*idx + idx_j] = img[idx_i, idx_j]
    print(result[26,29])

    fig = plt.figure(figsize=(1, 1))
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.05, hspace=0.05)
    ax = plt.subplot(gs[0])
    plt.axis('off')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')
    plt.imshow(result.reshape(img_size, width), cmap='Greys_r')
    return fig

def div2_draw(z,x1,x2,y1,y2):# 4개의 모양, 2개의 축을 이용하여 변화되는 모습을 그림
    x1 = z[x1]
    x2 = z[x2]
    y1 = z[y1]
    y2 = z[y2]
    for i in range(100):
        one = i % 10
        ten = int(i / 10)
        z[i] = ((x1 * (10 - one) + x2 * one) + (y1 * (10 - ten) + y2 * ten)) / 20
    return z


def div1_draw(z, x, y):
    x = z[x]
    y = z[y]
    z[0] = np.zeros(100)
    for i in range(1, 100):
        one = i % 10
        ten = int(i/10)
        z[i] = (x*one + y*ten)/(one+ten)
    return z

# 랜덤 출력 // 입력받은 문자열을 랜덤한 z_value로 출력한다.
def random_generate():
    input_text = input()
    generated_images = []

    for i in input_text:
        rand_num = randint(0, 100)
        idx = alphabet.index(i)
        generated_images.append(model_list[idx].predict(z_list[idx])[rand_num])
    return generated_images

def set_parameter_generate(z, ):

    return 0
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
model_list = []
z_list = []
for i in alphabet:
    model_list.append(load_model(i))
    z_list.append(load_z(i))

#z = div2_draw(z, 0,80, 65, 89)
#z = div1_draw(z, 0, 80)
#gererated_images = random_generate()


image_parameter = []

f = open('alphabet_parameter.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    image_parameter.append(line)
f.close()


while(1):
    input_text = input("출력할 텍스트를 입력해주세요: ")
    param_1 = int(input("첫번째 파라미터를 입력해주세요(굵기): "))
    param_2 = int(input("두번째 파라미터를 입력해주세요(기울기): "))
    param_3 = int(input("띄어쓰기 간격을 입력해주세요(1~5): "))
    generated_images = []
    for i in input_text:
        if i == " ":
            tmp = np.zeros((28, 28))
            tmp.fill(0)
            generated_images.append(tmp)
        else:
            idx = alphabet.index(i)
            param = image_parameter[idx][1:]
            param = list(map(int, param))
            param_list = []
            for j in param:
                param_list.append(z_list[idx][j])
            fin_z = (param_list[0]*(100-param_1) + param_list[1]*param_1 + param_list[2]*(100-param_2) + param_list[3]*param_2)/200
            fin_z = np.array(list(fin_z)*100).reshape(100,100)
            generated_images.append(model_list[idx].predict(fin_z)[0])

    result = img_attach(generated_images)
    plt.show()
    plt.close(result)

