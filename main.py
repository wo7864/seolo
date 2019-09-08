from keras.models import model_from_json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from random import *
import csv
# 만든 모델 리스트
phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
                , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ']
# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def load_z(font):
    z_value_list = []
    for phoneme in range(1, 27):
        with open("./z_value/{}/{}/{}.txt".format(font, phoneme, '450'), "r") as f:
            z_value = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
            z_value = z_value[1:-1].split(" ")
            z_value = [float(f) for f in z_value]
            z_value = np.array(z_value).reshape(100, 100)
            z_value_list.append(z_value)
    return z_value_list


def load_model(font):
    model_list = []
    for phoneme in range(1, 27):
        json_file = open("./model/{}/{}/{}.json".format(font, phoneme, '450'), "r")
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("./model/{}/{}/{}.h5".format(font, phoneme, '450'))
        model_list.append(loaded_model)
    return model_list


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


def ready():
    font_list = ['bangwool', 'bangwool_b', 'baram', 'baram_b', 'bawi', 'bawi_b', 'bburi', 'bidan', 'bidan_b', 'bori',
                'bori_b', 'buddle', 'buddle_b', 'dasle', 'goorm', 'groom_b', 'jandi', 'janggun', 'namu',
                'namu_b', 'namu_c', 'sandle', 'seassack', 'seassack_b', 'sonmut', 'sonmut_b', 'taepoong', 'yetdol']
    font_list = ['bangwool']

    model_list = []
    z_list = []
    for i in font_list:
        model_list.append(load_model(i))
        z_list.append(load_z(i))
    return font_list, model_list, z_list


def img_attach(imgs, text, latter_attach=70, phoneme_attach=18):
    save_dir = "./result/"
    latter_size = 84
    img_size = 28
    width = latter_attach*(len(imgs)-1)+img_size*2
    result = np.zeros((img_size, width*2))
    result.fill(1)
    for idx, latter in enumerate(imgs):
        for idx2, img in enumerate(latter):
            # Case 1: 모음 (ㅏ, ㅓ, ㅐ, ㅔ, ...)
            if 14 <= text[idx][1] <= 20:
                # Case 1-1: 종성 x
                if len(latter) == 2:
                    print("Case 1-1")
                # Case 1-2: 종성 o
                elif len(latter) == 3:
                    print("Case 1-2")
            # Case 2: 모음 ( ㅗ, ㅛ, ㅜ, ㅠ, ㅡ)
            elif 21 <= text[idx][1] <= 25:
                # Case 2-1: 종성 x
                if len(latter) == 2:
                    print("Case 2-1")
                # Case 2-2: 종성 o
                elif len(latter) == 3:
                    print("Case 2-2")
            # Case 3: 모음 (ㅘ, ㅙ, ㅚ, ㅝ, ...)
            else:
                # Case 3-1: 종성 x
                if len(latter) == 2:
                    print("Case 3-1")
                # Case 3-2: 종성 o
                elif len(latter) == 3:
                    print("Case 3-2")


            img = img.reshape(img_size, img_size)
            if idx == 0:
                result[:,:img_size] = img
            else:
                for idx_i, val_i in enumerate(img):
                    for idx_j, val_j in enumerate(val_i):
                        if img[idx_i, idx_j] <= result[idx_i, latter_attach*idx + phoneme_attach*idx2 + idx_j]:
                            result[idx_i, latter_attach*idx + phoneme_attach*idx2 + idx_j] = img[idx_i, idx_j]
    #result = abs(result-1)

    for idx, i in enumerate(result):
        for idx2, j in enumerate(i):
            if j < -0.3:
                result[idx][idx2] = -1
            elif j > 0.7:
                result[idx][idx2] = 1
    fig = plt.figure(figsize=(1, 1))
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.05, hspace=0.05)
    ax = plt.subplot(gs[0])
    plt.axis('off')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')
    plt.imshow(result, cmap='Greys_r')
    plt.show()
    #filename = save_dir + "{}_{}_{}_{}.png".format(text, p1, p2, attach)
    #fig.savefig(filename)

    return fig


# 4개의 모양, 2개의 축을 이용하여 변화되는 모습을 그림
def div2_draw(z,x1,x2,y1,y2):
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
def random_generate(font, model_list, z_list, text_list):
    generated_images = []

    for text in text_list:
        latter = []
        for i in text:
            if i!=26:
                rand_num = randint(0, 100)
                img = model_list[font][int(i)].predict(z_list[font][int(i)])[rand_num]
                latter.append(img)
        generated_images.append(latter)
    print(len(generated_images))
    return generated_images


def convert_text(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함.
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    for idx, i in enumerate(r_lst):
        for idx2, j in enumerate(i):
            r_lst[idx][idx2] = phoneme_list.index(j)
    return r_lst


def excute(font, model_list, z_list, text, p1, p2, p3, p4, p5):
    image_parameter = []
    generated_images = []
    generated_images = random_generate(font, model_list, z_list, text)
    result = img_attach(generated_images, text, p1, p2, p3, p4, p5)
    plt.show()
    plt.close(result)

if __name__ == "__main__":
    font_list, model_list, z_list = ready()
    font = font_list[0]
    text = convert_text("갸나더려")
    excute(0, model_list, z_list, text, 0, 100, 0, 0, 20)
