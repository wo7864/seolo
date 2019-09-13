from keras.models import model_from_json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from random import *
import csv
import cv2
import time
from PIL import Image

# 만든 모델 리스트
phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
    , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']



def load_z(font):
    z_value_list = []
    for phoneme in range(1, 27):
        with open("./z_value/{}/{}/{}.txt".format(font, phoneme, '450'), "r") as f:
            z_value = f.read().replace("\n", "").replace("[", " ").replace("]", " ")\
                .replace("  ", " ").replace("  "," ").replace("  ", " ")
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
    font_list = ['bangwool', 'baram_b']

    model_list = []
    z_list = []
    for i in font_list:
        model_list.append(load_model(i))
        z_list.append(load_z(i))
    return font_list, model_list, z_list


def img_attach(imgs, text, latter_attach=60, definition=30, color=0, phoneme_width_attach=30, phoneme_height_attach=30):
    save_dir = "./result/"
    latter_size = 84
    print(text)
    img_size1 = 28
    img_size2 = 42
    img_size3 = 84
    width = latter_attach * (len(imgs) - 1) + img_size1 * 2
    result = np.zeros((img_size3, width * 2))
    result.fill(1)
    width_point = 0
    height_point = 0
    for idx, latter in enumerate(imgs):
        # Case x: 띄어쓰기
        if text[idx][0] == 26:
            img = np.full([img_size3, img_size3], 1)
            for idx_i, val_i in enumerate(img):
                for idx_j, val_j in enumerate(val_i):
                    y = idx_i + height_point
                    x = latter_attach * width_point + idx_j
                    if img[idx_i, idx_j] <= result[y, x]:
                        result[y, x] = img[idx_i, idx_j]
        elif text[idx][0] == 27:
            height_point += 84
            width_point = -1
            tmp = np.full([img_size3, width * 2], 1)
            result = np.vstack([result, tmp])
        # Case 1: 모음 (ㅏ, ㅓ, ㅐ, ㅔ, ...)
        elif 14 <= text[idx][1] <= 20 and text[idx][2] == 26:
            # Case 1-1: 종성 x
            if text[idx][3] == 26:
                print("Case 1-1")
                for idx2, img in enumerate(latter):
                    if text[idx][idx2] != 26:
                        img = img.reshape(img_size1, img_size1)
                        img = cv2.resize(img, (img_size2, img_size2), interpolation=cv2.INTER_AREA)
                        tmp = np.full([int(img_size2/2), img_size2], 1)
                        img = np.vstack([tmp, img])
                        img = np.vstack([img, tmp])
                        for idx_i, val_i in enumerate(img):
                            for idx_j, val_j in enumerate(val_i):
                                y = idx_i + height_point
                                x = latter_attach * width_point + phoneme_width_attach * idx2 + idx_j
                                if img[idx_i, idx_j] <= result[y, x]:
                                    result[y, x] = img[idx_i, idx_j]
            # Case 1-2: 종성 o
            elif text[idx][3] != 26:
                print("Case 1-2")
                for idx2, img in enumerate(latter):
                    if text[idx][idx2] != 26:
                        img = img.reshape(img_size1, img_size1)
                        if idx2 < 2:
                            img = cv2.resize(img, (img_size2, img_size2), interpolation=cv2.INTER_AREA)
                            for idx_i, val_i in enumerate(img):
                                for idx_j, val_j in enumerate(val_i):
                                    y = idx_i + height_point
                                    x = latter_attach * width_point + phoneme_width_attach * idx2 + idx_j
                                    if img[idx_i, idx_j] <= result[y, x]:
                                        result[y, x] = img[idx_i, idx_j]
                        else:
                            img = cv2.resize(img, (img_size2, img_size2), interpolation=cv2.INTER_AREA)
                            for idx_i, val_i in enumerate(img):
                                for idx_j, val_j in enumerate(val_i):
                                    y = idx_i + phoneme_height_attach + height_point
                                    x = latter_attach * width_point + phoneme_width_attach + idx_j
                                    if img[idx_i, idx_j] <= result[y, x]:
                                        result[y, x] = img[idx_i, idx_j]
        # Case 2: 모음 ( ㅗ, ㅛ, ㅜ, ㅠ, ㅡ)
        elif 21 <= text[idx][1] <= 25 and text[idx][2] == 26:
            # Case 2-1: 종성 x
            if text[idx][3] == 26:
                print("Case 2-1")
                for idx2, img in enumerate(latter):
                    if text[idx][idx2] != 26:
                        img = img.reshape(img_size1, img_size1)
                        img = cv2.resize(img, (img_size2, img_size2), interpolation=cv2.INTER_AREA)
                        tmp = np.full([img_size2, int(img_size2 / 2)], 1)
                        img = np.hstack([tmp, img])
                        img = np.hstack([img, tmp])
                        for idx_i, val_i in enumerate(img):
                            for idx_j, val_j in enumerate(val_i):
                                y = int(idx_i + idx2 * (img_size2/2) + height_point)
                                x = latter_attach * width_point + idx_j
                                if img[idx_i, idx_j] <= result[y, x]:
                                    result[y, x] = img[idx_i, idx_j]
            # Case 2-2: 종성 o
            elif text[idx][3] != 26:
                print("Case 2-2")
                for idx2, img in enumerate(latter):
                    if text[idx][idx2] != 26:
                        img = img.reshape(img_size1, img_size1)
                        img = cv2.resize(img, (img_size2, img_size2), interpolation=cv2.INTER_AREA)
                        tmp = np.full([img_size2, int(img_size2 / 2)], 1)
                        img = np.hstack([tmp, img])
                        img = np.hstack([img, tmp])
                        if idx2 == 3:
                            idx2 = 2
                        for idx_i, val_i in enumerate(img):
                            for idx_j, val_j in enumerate(val_i):
                                y = int(idx_i + idx2 * (img_size2/2) + height_point)
                                x = latter_attach * width_point + idx_j
                                if img[idx_i, idx_j] <= result[y, x]:
                                    result[y, x] = img[idx_i, idx_j]
        # Case 3: 모음 (ㅘ, ㅙ, ㅚ, ㅝ, ...)
        else:
            # Case 3-1: 종성 x
            if text[idx][3] == 26:
                print("Case 3-1")
                for idx2, img in enumerate(latter):
                    if text[idx][idx2] != 26:
                        if idx2 == 0:
                            img = img.reshape(img_size1, img_size1)
                            for idx_i, val_i in enumerate(img):
                                for idx_j, val_j in enumerate(val_i):
                                    if img[idx_i, idx_j] <= result[idx_i + idx2 * img_size2 - 5 + height_point, latter_attach * width_point + idx_j]:
                                        result[idx_i + idx2 * img_size2 - 5 + height_point, latter_attach * width_point + idx_j] = img[idx_i, idx_j]
                        elif idx2 == 1:
                            img = img.reshape(img_size1, img_size1)
                            img = cv2.resize(img, (img_size2, img_size2), interpolation=cv2.INTER_AREA)
                            tmp = np.full([img_size2, int(img_size2 / 2)], 1)
                            img = np.hstack([tmp, img])
                            img = np.hstack([img, tmp])
                            for idx_i, val_i in enumerate(img):
                                for idx_j, val_j in enumerate(val_i):
                                    if img[idx_i, idx_j] <= result[idx_i + idx2 * img_size2 - 5 + height_point, latter_attach * width_point + idx_j]:
                                        result[idx_i + idx2 * img_size2 - 5 + height_point, latter_attach * width_point + idx_j] = img[idx_i, idx_j]

            # Case 3-2: 종성 o
            elif text[idx][3] != 26:
                print("Case 3-2")
        width_point += 1

    definition = (100 - definition) / 100
    # definition: 0~1
    for idx, i in enumerate(result):
        for idx2, j in enumerate(i):
            if j < definition*-1:
                result[idx][idx2] = -1
            elif j >= definition:
                result[idx][idx2] = 1

    # 색상 변경
    if color==1:
        result = result[:]*-1

    # 투명도
    tmp = np.full([result.shape[0], result.shape[1]], 1.0)
    for idx, i in enumerate(result):
        for idx2, j in enumerate(i):
            if color == 0:
                if j > 0:
                    tmp[idx][idx2] = 0.0
            else:
                if j <= 0:
                    tmp[idx][idx2] = 0.0

    print(tmp.shape)
    print(result.shape)
    print(tmp[0], tmp[50])
    result = cv2.merge((result, result, result, tmp))
    #result = Image.fromarray(result)
    #result = result.convert("RGB")
    #result = np.array(result)
    print(result)
    fig = plt.figure(figsize=(1, 1))
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.05, hspace=0.05)
    ax = plt.subplot(gs[0])
    plt.axis('off')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')
    plt.imshow(result, cmap='Greys_r')
    #plt.show()
    # filename = save_dir + "{}_{}_{}_{}.png".format(text, p1, p2, attach)
    # fig.savefig(filename)

    return fig


# 4개의 모양, 2개의 축을 이용하여 변화되는 모습을 그림
def div2_draw(z, x1, x2, y1, y2):
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
        ten = int(i / 10)
        z[i] = (x * one + y * ten) / (one + ten)
    return z


# 랜덤 출력 // 입력받은 문자열을 랜덤한 z_value로 출력한다.
def random_generate(font, model_list, z_list, text_list):
    generated_images = []
    rand_z = np.random.uniform(-1, 1, 10000)
    rand_z = rand_z.reshape(100, 100)
    for text in text_list:
        latter = []
        for i in text:
            if i < 26:
                rand_num = randint(0, 99)
                #img = model_list[font][int(i)].predict(z)[0]
                img = model_list[font][int(i)].predict(rand_z)[rand_num]
                latter.append(img)
            else:
                latter.append("")
        generated_images.append(latter)
    return generated_images


# 현재 불필요한 반복작업이 있음. 개선 필요
def convert_text(korean_word):
    chosung_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                     'ㅣ', ' ']
    jongsung_list = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                     'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    jungsung_list2 = [9, 10, 11, 14, 15, 16, 19]
    jungsung_list3 = [['ㅗ', 'ㅏ'], ['ㅗ', 'ㅐ'], ['ㅗ', 'ㅣ'], ['ㅜ', 'ㅓ'], ['ㅜ', 'ㅔ'],
                      ['ㅜ', 'ㅣ'], ['ㅡ', 'ㅣ']]
    r_lst = []
    for w in list(korean_word):
        # 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            # 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가')) // 588
            # 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch4 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            ch3 = 21
            if ch2 in jungsung_list2:
                idx = jungsung_list2.index(ch2)
                ch2 = jungsung_list.index(jungsung_list3[idx][0])
                ch3 = jungsung_list.index(jungsung_list3[idx][1])
            r_lst.append([chosung_list[ch1], jungsung_list[ch2], jungsung_list[ch3], jongsung_list[ch4]])
        else:
            r_lst.append([w])
    for idx, i in enumerate(r_lst):
        for idx2, j in enumerate(i):
            r_lst[idx][idx2] = phoneme_list.index(j)
    return r_lst


def main(font, text):
    font_list, model_list, z_list = ready()
    text = convert_text(text)
    latter_list = [100]
    for i in latter_list:
        start = time.time()
        generated_images = random_generate(font, model_list, z_list, text)
        result = img_attach(generated_images, text, i, 50, 0)
        print("time :", time.time() - start)
        plt.show()
        plt.close(result)

if __name__ == "__main__":
    input_text = "은하수"
    main(0, input_text)

# main(0, input_text, 10, 12, 13, 14, 15, 16)
# 색, 굵기, 서체 종류, 자모음간 거리
# 투명화: 수정 필요함. 정도에 따라 알파값 따로주기
# 하임, 돌하르방, 아름다운 한글, 은하수
# ㅎ, ㅇ, ㅏ, ㅣ, ㅁ, ㄷ, ㅗ, ㄹ, ㅂ, ㅡ, ㅜ, ㄴ, ㄱ, ㅅ
