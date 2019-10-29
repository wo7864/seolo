from keras.models import model_from_json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from random import *
import csv
import cv2
import time
from PIL import Image
import os
import tensorflow as tf
import infogan
from datetime import datetime
from urllib import parse
import json

# 만든 모델 리스트
phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
    , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']


def load_model(font):
    sess_list = []
    model_list = []
    for phoneme in range(1, 27):
        tf.reset_default_graph()
        sess = tf.Session()
        model = infogan.GAN(sess)
        model.saver.restore(sess, "./infogan_model/{}/{}_{}_{}.ckpt".format(phoneme, font, phoneme, '300'))
        model_list.append(model)
    sess_list.append(sess)
    return model_list, sess_list


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
    print("loading model...")
    font_list = ['bangwool', 'bangwool_b', 'baram', 'baram_b', 'bawi', 'bawi_b', 'bburi', 'bidan', 'bidan_b', 'bori',
                 'bori_b', 'buddle', 'buddle_b', 'dasle', 'goorm', 'groom_b', 'jandi', 'janggun', 'namu',
                 'namu_b', 'namu_c', 'sandle', 'seassack', 'seassack_b', 'sonmut', 'sonmut_b', 'taepoong', 'yetdol']
    font_list = ['bangwool']

    model_list = []
    sess_list = []
    for i in font_list:
        model, sess = load_model(i)
        model_list.append(model)
        sess_list.append(sess)
    print("complate!")
    return font_list, model_list, sess_list


'''
shape 종류
쌍자음이 아닌 초성
0: 모음: ㅏ, ㅓ, ㅣ... // 종성 0개
1: 모음: ㅏ, ㅓ, ㅣ... // 종성 1개
2: 모음: ㅏ, ㅓ, ㅣ... // 종성 2개
3: 모음: ㅗ, ㅜ, ㅡ... // 종성 0개
4: 모음: ㅗ, ㅜ, ㅡ... // 종성 1개
5: 모음: ㅗ, ㅜ, ㅡ... // 종성 2개
6: 모음: ㅚ, ㅢ, ㅟ... // 종성 0개
7: 모음: ㅚ, ㅢ, ㅟ... // 종성 1개
8: 모음: ㅚ, ㅢ, ㅟ... // 종성 2개
9: 모음: ㅖ, ㅒ        // 종성 0개
10: 모음: ㅖ, ㅒ       // 종성 1개
11: 모음: ㅖ, ㅒ       // 종성 2개

쌍자음 초성
12: 모음: ㅏ, ㅓ, ㅣ... // 종성 0개
13: 모음: ㅏ, ㅓ, ㅣ... // 종성 1개
14: 모음: ㅏ, ㅓ, ㅣ... // 종성 2개
15: 모음: ㅗ, ㅜ, ㅡ... // 종성 0개
16: 모음: ㅗ, ㅜ, ㅡ... // 종성 1개
17: 모음: ㅗ, ㅜ, ㅡ... // 종성 2개
18: 모음: ㅚ, ㅢ, ㅟ... // 종성 0개
19: 모음: ㅚ, ㅢ, ㅟ... // 종성 1개
20: 모음: ㅚ, ㅢ, ㅟ... // 종성 2개
21: 모음: ㅖ, ㅒ        // 종성 0개
22: 모음: ㅖ, ㅒ       // 종성 1개
23: 모음: ㅖ, ㅒ       // 종성 2개
'''


class Phoneme:
    def __init__(self, img, shape, latter_num, phoneme_num, x_point, y_point, param_list, phoneme, width, height):
        # shape 은 0~8까지. 모음과 종성의 개수에 따라 달라진다.
        self.shape = shape
        # 몇번째 글자인지.
        self.latter_num = latter_num
        # 해당 글자에서 몇번째를 차지 하는지. 초성, 초성2, 중성1, 중성2, 종성1, 종성2 총 6가지 경우를 갖는다.
        self.phoneme_num = phoneme_num
        # 파라미터 리스트. 총 5의 크기를 가지며 각 param은 -1~1의 값을 갖는다.
        self.param_list = param_list
        self.x = 0
        self.y = 0
        self.img = img
        self.phoneme = phoneme
        self.width = width
        self.height = height
        value = [x*7 for x in range(1, 10)]

        if shape == 0:
            if phoneme_num == 0:
                self.y = value[2]
            elif phoneme_num == 2:
                self.x = value[3]
                self.y = value[2]
        elif shape == 1:
            if phoneme_num == 0:
                self.y = value[0]
            elif phoneme_num == 2:
                self.x = value[3]
                self.y = value[0]
            elif phoneme_num == 4:
                self.x = value[3]
                self.y = value[5]
        elif shape == 2:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 2:
                self.x = value[5]
            elif phoneme_num == 4:
                self.y = value[5]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[5]
        elif shape == 3:
            if phoneme_num == 0:
                self.y = value[2]
            elif phoneme_num == 2:
                self.y = value[4]
        elif shape == 4:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 4:
                self.y = value[6]
        elif shape == 5:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 4:
                self.y = value[6]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[6]
        elif shape == 6:
            if phoneme_num == 0:
                self.y = value[3]
            elif phoneme_num == 2:
                self.y = value[5]
            elif phoneme_num == 3:
                self.x = value[5]
                self.y = value[3]
        elif shape == 7:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 3:
                self.x = value[5]
            elif phoneme_num == 4:
                self.x = value[5]
                self.y = value[5]
        elif shape == 8:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 3:
                self.x = value[3]
            elif phoneme_num == 4:
                self.y = value[6]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[6]
        elif shape == 9:
            if phoneme_num == 0:
                self.y = value[2]
            elif phoneme_num == 2:
                self.x = value[3]
                self.y = value[2]
            elif phoneme_num == 3:
                self.x = value[4]
        elif shape == 10:
            if phoneme_num == 0:
                self.y = value[0]
            elif phoneme_num == 2:
                self.x = value[3]
                self.y = value[0]
            elif phoneme_num == 3:
                self.x = value[4]
            elif phoneme_num == 4:
                self.x = value[3]
                self.y = value[5]
        elif shape == 11:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 2:
                self.x = value[3]
            elif phoneme_num == 3:
                self.x = value[4]
            elif phoneme_num == 4:
                self.y = value[5]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[5]
        elif shape == 12:
            if phoneme_num == 0:
                self.y = value[2]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[2]
            elif phoneme_num == 2:
                self.x = value[4]
                self.y = value[2]
        elif shape == 13:
            if phoneme_num == 0:
                self.y = value[0]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[0]
            elif phoneme_num == 2:
                self.x = value[4]
                self.y = value[0]
            elif phoneme_num == 4:
                self.x = value[3]
                self.y = value[5]
        elif shape == 14:
            if phoneme_num == 0:
                self.y = value[0]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[0]
            elif phoneme_num == 2:
                self.x = value[4]
            elif phoneme_num == 4:
                self.y = value[5]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[5]
        elif shape == 15:
            if phoneme_num == 0:
                self.y = value[2]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[2]
            elif phoneme_num == 2:
                self.y = value[4]
        elif shape == 16:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 1:
                self.x = value[2]
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 4:
                self.y = value[6]
        elif shape == 17:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 1:
                self.x = value[2]
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 4:
                self.y = value[6]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[6]
        elif shape == 18:
            if phoneme_num == 0:
                self.y = value[3]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[3]
            elif phoneme_num == 2:
                self.y = value[5]
            elif phoneme_num == 3:
                self.x = value[5]
                self.y = value[3]
        elif shape == 19:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 1:
                self.x = value[2]
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 3:
                self.x = value[5]
            elif phoneme_num == 4:
                self.x = value[5]
                self.y = value[5]
        elif shape == 20:
            if phoneme_num == 0:
                pass
            elif phoneme_num == 1:
                self.x = value[2]
            elif phoneme_num == 2:
                self.y = value[3]
            elif phoneme_num == 3:
                self.x = value[3]
            elif phoneme_num == 4:
                self.y = value[6]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[6]
        elif shape == 21:
            if phoneme_num == 0:
                self.y = value[2]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[2]
            elif phoneme_num == 2:
                self.x = value[3]
                self.y = value[2]
            elif phoneme_num == 3:
                self.x = value[4]
        elif shape == 22:
            if phoneme_num == 0:
                self.y = value[0]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[0]
            elif phoneme_num == 2:
                self.x = value[3]
                self.y = value[0]
            elif phoneme_num == 3:
                self.x = value[4]
            elif phoneme_num == 4:
                self.x = value[3]
                self.y = value[5]
        elif shape == 23:
            if phoneme_num == 0:
                self.y = value[0]
            elif phoneme_num == 1:
                self.x = value[2]
                self.y = value[0]
            elif phoneme_num == 2:
                self.x = value[3]
            elif phoneme_num == 3:
                self.x = value[4]
            elif phoneme_num == 4:
                self.y = value[5]
            elif phoneme_num == 5:
                self.x = value[3]
                self.y = value[5]
        self.x += x_point
        self.y += y_point

'''
class latter:
    def __init__(self, pho_list):
        self.left = 9999999999
        self.right = 0
        self.top = 999999999
        self.bottom = 0
        for pho in pho_list:
            if pho.img.shape[1] + pho.x > self.right:
                self.right = pho.img.shape[1] + pho.x
            if pho.x < self.left:
                self.left = pho.x
            if pho.img.shape[0] + pho.y > self.bottom:
                self.bottom = pho.img.shape[0] + pho.y
            if pho.y < self.top:
                self.top = pho.y
'''

def add_image(paper, image, width_point, height_point):
    for idx_i, val_i in enumerate(image):
        for idx_j, val_j in enumerate(val_i):
            y = idx_i + height_point
            x = idx_j + width_point
            if image[idx_i, idx_j] <= paper[y, x]:
                paper[y, x] = image[idx_i, idx_j]
    return paper


def set_definition(result, definition):
    definition = (100 - definition) / 100
    # definition: 0~1
    for idx, i in enumerate(result):
        for idx2, j in enumerate(i):
            if j < definition * -1:
                result[idx][idx2] = -1
            elif j >= definition:
                result[idx][idx2] = 1
    return result


def set_invisibility(result, color):
    tmp = np.full([result.shape[0], result.shape[1]], 1.0)
    for idx, i in enumerate(result):
        for idx2, j in enumerate(i):
            if color == 0:
                if j == 1:
                    tmp[idx][idx2] = 1 - j
            else:
                if j == -1:
                    tmp[idx][idx2] = 1 + j

    result = cv2.merge((result, result, result, tmp))
    return result

def json_to_obj(text):
    latter_list = []
    for latter in text:
        phoneme_list2 = []
        for phoneme in latter:
            phoneme_list2.append(Phoneme(np.array(phoneme['img']), phoneme['shape_list'], phoneme['latter_num'],
                                 phoneme['phoneme_num'], phoneme['x'], phoneme['y'], phoneme['params'],
                                 phoneme['phoneme'], phoneme['width'], phoneme['height']))
        latter_list.append(phoneme_list2)
    return latter_list


def create_latter_list(font, model_list, sess_list, text, shape_list, param_list2):
    # 각 음소간에 좌표를 지정하여 phoneme 인스턴스 생성
    latter_list = []
    small_list = [3, 4, 5, 15, 16, 17]
    x_point = 0
    y_point = 0
    pre_pho = None
    json_latter_list = []
    for idx, latter in enumerate(text):
        phoneme_list2 = []
        json_pho_list = []
        for idx2, pho in enumerate(latter):
            if text[idx][idx2] != 26:
                img = gen_image(pho, model_list[font][pho], sess_list[font][pho], param_list2)
                phoneme_list2.append(Phoneme(img, shape_list[idx], idx, idx2, x_point, y_point,
                                             param_list2, phoneme_list[text[idx][idx2]], img.shape[1], img.shape[0]))
                param_list = [0] * 4
                json_pho = {
                    "img": img.tolist(),
                    "shape_list": shape_list[idx],
                    "latter_num": idx,
                    "phoneme_num": idx2,
                    "x": x_point,
                    "y": y_point,
                    "params": param_list,
                    "phoneme": phoneme_list[text[idx][idx2]],
                    "width":img.shape[1],
                    "height":img.shape[0]
                }
                json_pho_list.append(json_pho)
            else:
                phoneme_list2.append('')

        if shape_list[idx] in small_list:
            x_point += 28
        else:
            x_point += 56
        latter_list.append(phoneme_list2)
        json_latter_list.append(json_pho_list)
    return latter_list, json_latter_list


def set_color(result, color):
    r = np.full([result.shape[0], result.shape[1]], color[0])
    g = np.full([result.shape[0], result.shape[1]], color[1])
    b = np.full([result.shape[0], result.shape[1]], color[2])
    r = r[:] / 1
    g = g[:] / 1
    b = b[:] / 1
    result = 1 - result[:]
    result = result[:] * 255
    result = cv2.merge((r, g, b, result))
    result = result.astype(np.uint8)
    result = Image.fromarray(result, 'RGBA')
    return result


def img_attach(latter_list, definition, color, ori_text, image_width=None, image_height=None):
    left = 9999999999
    right = 0
    top = 999999999
    bottom = 0
    for idx, latter in enumerate(latter_list):
        for idx2, pho in enumerate(latter):
            if not isinstance(pho, str):
                if pho.img != "":
                    if pho.img.shape[1] + pho.x > right:
                        right = pho.img.shape[1] + pho.x
                    if pho.x < left:
                        left = pho.x
                    if pho.img.shape[0] + pho.y > bottom:
                        bottom = pho.img.shape[0] + pho.y
                    if pho.y < top:
                        top = pho.y

    if left < 0:
        for idx, latter in enumerate(latter_list):
            for idx2, pho in enumerate(latter):
                if not isinstance(pho, str):
                    if pho.img != "":
                        pho.x += 0-left

    if top < 0:
        for idx, latter in enumerate(latter_list):
            for idx2, pho in enumerate(latter):
                if not isinstance(pho, str):
                    if pho.img != "":
                        pho.y += 0-top

    width = right - left
    height = bottom - top
    if height < 84:
        height = 84
    result = np.zeros((height+1, width+1))
    result.fill(1)

    # phoneme 인스턴스의 위치좌표에 따라 생성된 이미지를 결합
    for idx, latter in enumerate(latter_list):
        for idx2, pho in enumerate(latter):
            if not isinstance(pho, str):
                if pho.img != "":
                    result = add_image(result, pho.img, pho.x, pho.y)

    if not image_width:
        image_width = result.shape[1] * 5
    if not image_height:
        image_height = result.shape[0] * 5
    # 각 길이를 5배로 확장
    result = cv2.resize(result, (image_width, image_height), interpolation=cv2.INTER_LINEAR)

    # 선명도 조절
    result = set_definition(result, definition)

    # 색 지정
    result = set_color(result, color)

    now = datetime.now()
    filename = ori_text + now.strftime("_%m_%d_%Y_%H_%M_%S.png")
    save_dir = 'static/image/'
    result.save(save_dir + filename)
    return filename


def blur(img):
    width = img.shape[1]
    height = img.shape[0]
    tmp = np.full((1, 28), 1)
    tmp2 = np.full((30, 1), 1)
    img = np.vstack([img, tmp])
    img = np.vstack([tmp, img])
    img = np.hstack([img, tmp2])
    img = np.hstack([tmp2, img])
    update_list = []
    for x in range(1, width-1):
        for y in range(1, height-1):
            value = img[y-1][x-1] + img[y][x-1] + img[y+1][x-1] \
            + img[y-1][x] + img[y+1][x] + img[y-1][x+1] + img[y][x+1] + img[y+1][x+1]
            value /= 8
            if img[y][x] + 0.5 <value:
                update_list.append((x, y, value))
    for i in update_list:
        img[i[1]][i[0]] = i[2]
    return img


def gen_image(text, model, sess, param_list):
    num_generate = 1
    if text < 26:
        #noise = model.Generate_noise(1)  # noise = (num_generate, model.noise_dim)
        noise = np.full((1, 62), 0)
        noise = np.tile(noise, [num_generate, 1])
        latent_code = np.zeros([num_generate, 4])
        for idx, param in enumerate(param_list):
            latent_code[:, idx] = param
        generated = sess.run(model.Gen, {  # num_generate, 28, 28, 1
            model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
        }
                                 )
        img = np.reshape(generated, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width
        img = blur(img)
        return img
    else:
        return ''

def remove_noise(img):
    print(img)
    width = img.shape[1]
    height = img.shape[0]
    val = 4
    for x in range(width-val):
        for y in range(height-val):
            swi = 0
            for i in range(val):
                if img[y][x+i] <= 1.0:
                        swi = 1
                if img[y+val][x+i] <= 1.0:
                        swi = 1
                if img[y+i][x] <= 1.0:
                        swi = 1
                if img[y+i][x+val] <= 1.0:
                        swi = 1
            if swi == 0:
                img[y+1:y+val][x+1:x+val] = 1
    return img
'''
def gen_image(font, text_list, model_list, sess_list, param_list):
    start_value = 1
    num_generate = 1
    imgs = []
    for text in text_list:
        latter = []
        for i in text:
            if i < 26:
                model = model_list[int(i)]
                sess = sess_list[int(i)]
                noise = model.Generate_noise(1)  # noise = (num_generate, model.noise_dim)
                noise = np.tile(noise, [num_generate, 1])

                space = 10
                c = np.linspace(start_value, -start_value, space)  # start_value ~ -start_value를 num_generate 등분.

                latent_code = np.zeros([num_generate, 5])
                for idx, param in enumerate(param_list):
                    latent_code[:, idx] = param
                generated = sess.run(model.Gen, {  # num_generate, 28, 28, 1
                    model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
                }
                                     )
                generated = np.reshape(generated,
                                       (model.height, model.width))  # 이미지 형태로. #num_generate, height, width
                latter.append(generated)
            else:
                latter.append("")
        imgs.append(latter)
    return imgs
'''


def create_one_image(phoneme, model, sess):
    noise = np.full((1, 62), 0)
    noise = np.tile(noise, [1, 1])
    latent_code = np.zeros([1, 4])
    for idx, param in enumerate(phoneme.param_list):
        latent_code[:, idx] = (int(param)/50) - 1
    generated = sess.run(model.Gen, {  # num_generate, 28, 28, 1
        model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
    })
    img = np.reshape(generated, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width
    return img


# 현재 불필요한 반복작업이 있음. 개선 필요
def convert_text(korean_word):
    chosung_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', ' ']
    chosung_list2 = [1, 4, 8, 10, 13] # ㄲ, ㄸ, ㅃ, ㅉ ...

    jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                     'ㅣ', ' ']
    jungsung_list2 = [9, 10, 11, 14, 15, 16, 19] # ㅚ, ㅟ, ㅢ , ㅞ ...
    jungsung_list3 = [['ㅗ', 'ㅏ'], ['ㅗ', 'ㅐ'], ['ㅗ', 'ㅣ'], ['ㅜ', 'ㅓ'], ['ㅜ', 'ㅔ'],
                      ['ㅜ', 'ㅣ'], ['ㅡ', 'ㅣ']]
    jungsung_list4 = [8, 12, 13, 17, 18] # ㅗ, ㅜ, ㅡ, ...
    jungsung_list5 = [3, 7] # ㅒ, ㅖ
    jungsung_list6 = [['ㅑ', 'ㅣ'], ['ㅕ', 'ㅣ']]

    jongsung_list = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                     'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    jongsung_list2 = [2, 3, 5, 6, 9, 10, 11, 12, 13, 14, 15, 18, 20] # ㄲ, ㄳ, ㄵ, ㄶ, ...
    jongsung_list3 = [['ㄱ', 'ㄱ'], ['ㄱ', 'ㅅ'], ['ㄴ', 'ㅈ'], ['ㄴ', 'ㅎ'], ['ㄹ', 'ㄱ'], ['ㄹ', 'ㅁ'], ['ㄹ', 'ㅂ'],
                      ['ㄹ', 'ㅅ'], ['ㄹ', 'ㅌ'], ['ㄹ', 'ㅍ'], ['ㄹ', 'ㅎ'], ['ㅂ', 'ㅅ'], ['ㅅ', 'ㅅ']]

    r_lst = []
    shape_list = []

    for w in list(korean_word):
        if not isinstance(w, list):
            shape = -1
            # 영어인 경우 구분해서 작성함.
            if '가' <= w <= '힣':
                shape += 1
                # 588개 마다 초성이 바뀜.
                ch1 = (ord(w) - ord('가')) // 588
                # 중성은 총 28가지 종류
                ch3 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
                ch5 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch3
                ch2 = 19
                ch4 = 21
                ch6 = 0

                if ch3 in jungsung_list4:
                    shape += 3

                if ch5 != 0:
                    shape += 1

                if ch1 in chosung_list2:
                    ch2 = ch1 - 1
                    ch1 = ch2
                    shape += 12

                if ch3 in jungsung_list2:
                    idx = jungsung_list2.index(ch3)
                    ch3 = jungsung_list.index(jungsung_list3[idx][0])
                    ch4 = jungsung_list.index(jungsung_list3[idx][1])
                    shape += 6

                elif ch3 in jungsung_list5:
                    idx = jungsung_list5.index(ch3)
                    ch3 = jungsung_list.index(jungsung_list6[idx][0])
                    ch4 = jungsung_list.index(jungsung_list6[idx][1])
                    shape += 9

                if ch5 in jongsung_list2:
                    idx = jongsung_list2.index(ch5)
                    ch5 = jongsung_list.index(jongsung_list3[idx][0])
                    ch6 = jongsung_list.index(jongsung_list3[idx][1])
                    shape += 1

                r_lst.append([chosung_list[ch1], chosung_list[ch2], jungsung_list[ch3], jungsung_list[ch4], jongsung_list[ch5], jongsung_list[ch6]])
            else:
                r_lst.append([w])
            shape_list.append(shape)
    for idx, i in enumerate(r_lst):
        for idx2, j in enumerate(i):
            r_lst[idx][idx2] = phoneme_list.index(j)
    return r_lst, shape_list


def main(model_list, sess_list, ori_text, latter_attach, definition, color, filename):

    text, shape_list = convert_text(ori_text)
    param_list = [50] * 5
    param_list = [(x/50)-1 for x in param_list]
    #generated_images = gen_image(0, text, model_list[0], sess_list[0], param_list)
    latter_list = create_latter_list(model_list[0], sess_list[0], text, shape_list, param_list)
    result = img_attach(latter_list, latter_attach, definition, color, ori_text)
    #img = create_one_image(font, model_list, 7)
    #generated_images[0][0] = img
    #latter_list[0][0].y += 10

if __name__ == "__main__":
    font_list, model_list, sess_list = ready()
    input_text = "안녕하세요"
    fontList = [0, 1, 2]
    latter_attach_list = [50, 75, 100]
    definition_list = [10, 50, 100]
    color_list = [0, 1]
    main(model_list, sess_list, input_text, latter_attach_list[0], definition_list[0], color_list[0], "test")
