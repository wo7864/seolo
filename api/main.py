import numpy as np
import cv2
from PIL import Image
from datetime import datetime
import os

# 만든 모델 리스트
phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
    , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']

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
    def __init__(self, img, shape, latter_num, phoneme_num, x_point, y_point, param_list, phoneme, width, height, rotation):
        # shape 은 0~8까지. 모음과 종성의 개수에 따라 달라진다.
        self.shape = shape
        # 몇번째 글자인지.
        self.latter_num = latter_num
        # 해당 글자에서 몇번째를 차지 하는지. 초성, 초성2, 중성1, 중성2, 종성1, 종성2 총 6가지 경우를 갖는다.
        self.phoneme_num = phoneme_num
        # 파라미터 리스트. 총 5의 크기를 가지며 각 param은 -1~1의 값을 갖는다.
        self.param_list = param_list
        self.x = x_point
        self.y = y_point
        self.img = img
        self.phoneme = phoneme
        self.width = width
        self.height = height
        self.rotation = rotation

    def set_location(self):
        value = [x*16 for x in range(1, 10)]
        if self.shape == 0:
            if self.phoneme_num == 0:
                self.y += value[2]
            elif self.phoneme_num == 2:
                self.x += value[3]
                self.y += value[2]
        elif self.shape == 1:
            if self.phoneme_num == 0:
                self.y += value[0]
            elif self.phoneme_num == 2:
                self.x += value[3]
                self.y += value[0]
            elif self.phoneme_num == 4:
                self.x += value[3]
                self.y += value[5]
        elif self.shape == 2:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 2:
                self.x += value[5]
            elif self.phoneme_num == 4:
                self.y += value[5]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[5]
        elif self.shape == 3:
            if self.phoneme_num == 0:
                self.y += value[2]
            elif self.phoneme_num == 2:
                self.y += value[4]
        elif self.shape == 4:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 4:
                self.y += value[6]
        elif self.shape == 5:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 4:
                self.y += value[6]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[6]
        elif self.shape == 6:
            if self.phoneme_num == 0:
                self.y += value[3]
            elif self.phoneme_num == 2:
                self.y += value[5]
            elif self.phoneme_num == 3:
                self.x += value[5]
                self.y += value[3]
        elif self.shape == 7:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 3:
                self.x += value[5]
            elif self.phoneme_num == 4:
                self.x += value[5]
                self.y += value[5]
        elif self.shape == 8:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 3:
                self.x += value[3]
            elif self.phoneme_num == 4:
                self.y += value[6]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[6]
        elif self.shape == 9:
            if self.phoneme_num == 0:
                self.y += value[2]
            elif self.phoneme_num == 2:
                self.x += value[3]
                self.y += value[2]
            elif self.phoneme_num == 3:
                self.x += value[4]
        elif self.shape == 10:
            if self.phoneme_num == 0:
                self.y += value[0]
            elif self.phoneme_num == 2:
                self.x += value[3]
                self.y += value[0]
            elif self.phoneme_num == 3:
                self.x += value[4]
            elif self.phoneme_num == 4:
                self.x += value[3]
                self.y += value[5]
        elif self.shape == 11:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 2:
                self.x += value[3]
            elif self.phoneme_num == 3:
                self.x += value[4]
            elif self.phoneme_num == 4:
                self.y += value[5]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[5]
        elif self.shape == 12:
            if self.phoneme_num == 0:
                self.y += value[2]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[2]
            elif self.phoneme_num == 2:
                self.x += value[4]
                self.y += value[2]
        elif self.shape == 13:
            if self.phoneme_num == 0:
                self.y += value[0]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[0]
            elif self.phoneme_num == 2:
                self.x += value[4]
                self.y += value[0]
            elif self.phoneme_num == 4:
                self.x += value[3]
                self.y += value[5]
        elif self.shape == 14:
            if self.phoneme_num == 0:
                self.y += value[0]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[0]
            elif self.phoneme_num == 2:
                self.x += value[4]
            elif self.phoneme_num == 4:
                self.y += value[5]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[5]
        elif self.shape == 15:
            if self.phoneme_num == 0:
                self.y += value[2]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[2]
            elif self.phoneme_num == 2:
                self.y += value[4]
        elif self.shape == 16:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 1:
                self.x += value[2]
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 4:
                self.y += value[6]
        elif self.shape == 17:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 1:
                self.x += value[2]
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 4:
                self.y += value[6]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[6]
        elif self.shape == 18:
            if self.phoneme_num == 0:
                self.y += value[3]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[3]
            elif self.phoneme_num == 2:
                self.y += value[5]
            elif self.phoneme_num == 3:
                self.x += value[5]
                self.y += value[3]
        elif self.shape == 19:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 1:
                self.x += value[2]
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 3:
                self.x += value[5]
            elif self.phoneme_num == 4:
                self.x += value[5]
                self.y += value[5]
        elif self.shape == 20:
            if self.phoneme_num == 0:
                pass
            elif self.phoneme_num == 1:
                self.x += value[2]
            elif self.phoneme_num == 2:
                self.y += value[3]
            elif self.phoneme_num == 3:
                self.x += value[3]
            elif self.phoneme_num == 4:
                self.y += value[6]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[6]
        elif self.shape == 21:
            if self.phoneme_num == 0:
                self.y += value[2]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[2]
            elif self.phoneme_num == 2:
                self.x += value[3]
                self.y += value[2]
            elif self.phoneme_num == 3:
                self.x += value[4]
        elif self.shape == 22:
            if self.phoneme_num == 0:
                self.y += value[0]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[0]
            elif self.phoneme_num == 2:
                self.x += value[3]
                self.y += value[0]
            elif self.phoneme_num == 3:
                self.x += value[4]
            elif self.phoneme_num == 4:
                self.x += value[3]
                self.y += value[5]
        elif self.shape == 23:
            if self.phoneme_num == 0:
                self.y += value[0]
            elif self.phoneme_num == 1:
                self.x += value[2]
                self.y += value[0]
            elif self.phoneme_num == 2:
                self.x += value[3]
            elif self.phoneme_num == 3:
                self.x += value[4]
            elif self.phoneme_num == 4:
                self.y += value[5]
            elif self.phoneme_num == 5:
                self.x += value[3]
                self.y += value[5]


def add_image(paper, image, width_point, height_point):
    for idx_i, val_i in enumerate(image):
        for idx_j, val_j in enumerate(val_i):
            y = idx_i + height_point
            x = idx_j + width_point
            if image[idx_i, idx_j] <= paper[y, x]:
                paper[y, x] = image[idx_i, idx_j]
    return paper


def set_definition(result, definition=90):
    definition = definition / 200
    # definition: 0~1
    for idx, i in enumerate(result):
        for idx2, j in enumerate(i):
            if j > 1-definition:
                result[idx][idx2] = 1
            elif j <= definition:
                result[idx][idx2] = 0
    return result


def normalization(result):
    min_value = np.min(result)
    result = result[:] - min_value
    max_value = np.max(result)
    result = result[:] / max_value
    return result


def json_to_obj(text):
    latter_list = []
    for latter in text:
        phoneme_list2 = []
        for phoneme in latter:
            phoneme_list2.append(Phoneme(np.array(phoneme['img']), phoneme['shape_list'], phoneme['latter_num'],
                                 phoneme['phoneme_num'], phoneme['x'], phoneme['y'], phoneme['params'],
                                 phoneme['phoneme'], phoneme['width'], phoneme['height'], phoneme['rotation']))
        latter_list.append(phoneme_list2)
    return latter_list


def create_latter_list(font, model_list, sess_list, text, shape_list, param_list2):
    # 각 음소간에 좌표를 지정하여 phoneme 인스턴스 생성
    latter_list = []
    small_list = [3, 4, 5, 15, 16, 17]
    x_point = 0
    y_point = 0
    rotation = 0
    json_latter_list = []
    for idx, latter in enumerate(text):
        phoneme_list2 = []
        json_pho_list = []
        for idx2, pho in enumerate(latter):
            if text[idx][idx2] != 26:
                img = gen_image(pho, model_list[font][pho], sess_list[font][pho], param_list2)
                phoneme = Phoneme(img, shape_list[idx], idx, idx2, x_point, y_point,
                                  param_list2, phoneme_list[text[idx][idx2]], img.shape[1], img.shape[0], rotation)
                phoneme.set_location()
                phoneme_list2.append(phoneme)
                param_list = [50] * 4
                json_pho = {
                    "img": img.tolist(),
                    "shape_list": shape_list[idx],
                    "latter_num": idx,
                    "phoneme_num": idx2,
                    "x": phoneme.x,
                    "y": phoneme.y,
                    "params": param_list,
                    "phoneme": phoneme_list[text[idx][idx2]],
                    "width": img.shape[1],
                    "height": img.shape[0],
                    "rotation": rotation
                }
                json_pho_list.append(json_pho)
            else:
                phoneme_list2.append('')

        if shape_list[idx] in small_list:
            x_point += 64
        else:
            x_point += 128
        latter_list.append(phoneme_list2)
        json_latter_list.append(json_pho_list)
    return latter_list, json_latter_list


def set_color_rgba(result, color):
    r = np.full([result.shape[0], result.shape[1]], color[0])
    g = np.full([result.shape[0], result.shape[1]], color[1])
    b = np.full([result.shape[0], result.shape[1]], color[2])
    r = r[:] / 1
    g = g[:] / 1
    b = b[:] / 1
    result = 1 - result[:]
    result = result[:] * 255
    img2 = []
    for i in range(result.shape[0]):
        tmp = []
        for j in range(result.shape[1]):
            tmp.append([r[i][j], g[i][j], b[i][j], result[i][j]])
        img2.append(tmp)
    img2 = np.array(img2)
    result = img2.astype(np.uint8)
    result = Image.fromarray(result, 'RGBA')
    return result


def set_color_rgb(result):
    result = result[:] * 255
    img2 = []
    for i in range(result.shape[0]):
        tmp = []
        for j in range(result.shape[1]):
            tmp.append([result[i][j], result[i][j], result[i][j]])
        img2.append(tmp)
    img2 = np.array(img2)
    result = img2.astype(np.uint8)
    result = Image.fromarray(result, 'RGB')
    return result


def img_attach(latter_list, blur_value, color, is_invisiable, ori_text, bg_data, image_width=None, image_height=None):
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

    width = right
    height = bottom
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
        image_width = result.shape[1] * 2
    if not image_height:
        image_height = result.shape[0] * 2

    result = cv2.blur(result, (blur_value * 2 + 1, blur_value * 2 + 1), 0)
    # 각 길이를 5배로 확장
    result = cv2.resize(result, (image_width, image_height), interpolation=cv2.INTER_LINEAR)

    # 색 지정
    if is_invisiable:
        result = set_color_rgba(result, color)
    else:
        result = set_color_rgb(result)

    now = datetime.now()
    filename = ori_text + now.strftime("%m_%d_%Y_%H_%M_%S.png")
    save_dir = 'static/image/'
    result.save(save_dir + filename)
    com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
    os.system(com)

    cb_filename = ''
    if bg_data:
        bg_file = Image.open(save_dir + bg_data[0])
        cb_filename = combine_bg(result, bg_file, ori_text, bg_data[1], bg_data[2])
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(cb_filename)
        os.system(com)

    return filename, cb_filename, image_width, image_height


def blur(img, limit=0.5):
    width = img.shape[1]
    height = img.shape[0]
    tmp = np.full((1, width), 1)
    tmp2 = np.full((height+2, 1), 1)
    img = np.vstack([img, tmp])
    img = np.vstack([tmp, img])
    img = np.hstack([img, tmp2])
    img = np.hstack([tmp2, img])
    update_list = []
    for x in range(1, width+1):
        for y in range(1, height+1):
            value = img[y-1][x-1] + img[y][x-1] + img[y+1][x-1] + img[y-1][x] + img[y+1][x] + img[y-1][x+1] + \
                    img[y][x+1] + img[y+1][x+1]
            value /= 8
            if limit < value:
                update_list.append((x, y, value))
    for i in update_list:
        img[i[1]][i[0]] = limit+0.1
    return img


def gen_image(text, model, sess, param_list):
    if text < 26:
        noise = np.full((1, 50), (int(param_list[3])/50) - 1)
        noise = np.tile(noise, [1, 1])
        latent_code = np.zeros([1, 3])
        for idx in range(3):
            latent_code[:, idx] = (int(param_list[idx])/50) - 1
        generated = sess.run(model.Gen, {  # num_generate, 28, 28, 1
            model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
        }
        )

        img = np.reshape(generated, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width
        img = normalization(img)
        width = int(img.shape[1] / 4)
        height = int(img.shape[0] / 4)
        tmp = np.full((width, width*4), 1)
        tmp2 = np.full((height*4 + (width * 2), height), 1)
        img = np.vstack([img, tmp])
        img = np.vstack([tmp, img])
        img = np.hstack([img, tmp2])
        img = np.hstack([tmp2, img])

        img = blur(img)
        img = set_definition(img)
        return img
    else:
        return ''


def create_sample_image(font, text, model, sess, param_list):
    file_list = []
    for i in range(4):
        for j in range(0, 101, 100):
            tmp = param_list[i]
            param_list[i] = j
            filename = '{}_{}_{}_{}_{}_{}.png'.format(font, text, param_list[0], param_list[1], param_list[2], param_list[3])
            save_dir = 'static/image/sample/'
            f = save_dir + filename
            if not os.path.isfile(f):
                img = gen_image(text, model, sess, param_list)
                img = img[:] * 255
                img = img.astype(np.uint8)
                img = Image.fromarray(img, 'L')
                img.save(f)
                file_list.append(f)
            param_list[i] = tmp
    com = 's3cmd put '
    for f in file_list:
        com += f
        com += ' '
    com += 's3://seolo/static/image/sample/'
    print(com)
    os.system(com)
    return 0


def update_rotation(img2, rotation):
    img2 = img2.astype(np.uint8)
    matrix = cv2.getRotationMatrix2D((img2.shape[1]/2, img2.shape[0]/2), int(rotation)*-1, 1)
    img2 = cv2.warpAffine(img2, matrix, (img2.shape[1], img2.shape[0]),  borderMode=cv2.BORDER_REPLICATE)
    return img2


def create_one_image(phoneme, model, sess):

    noise = np.full((1, 50), phoneme.param_list[0])
    params = phoneme.param_list[1:]
    noise = np.tile(noise, [1, 1])
    latent_code = np.zeros([1, 3])
    for idx, param in enumerate(params):
        latent_code[:, idx] = (int(param)/50) - 1

    generated = sess.run(model.Gen, {
        model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
    })
    img = np.reshape(generated, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width
    print(img)
    img = normalization(img)
    print(img)
    width = int(img.shape[1] / 4)
    height = int(img.shape[0] / 4)
    tmp = np.full((width, width * 4), 1)
    tmp2 = np.full((height * 4 + (width * 2), height), 1)
    img = np.vstack([img, tmp])
    img = np.vstack([tmp, img])
    img = np.hstack([img, tmp2])
    img = np.hstack([tmp2, img])

    #img = blur(img)
    #img = set_definition(img)
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


def bg_file_save(bg_file, text):
    save_dir = 'static/image/'
    now = datetime.now()
    filename = 'bg_' + text + now.strftime("_%m_%d_%Y_%H_%M_%S.png")
    background_image = Image.open(bg_file)
    background_image.save(save_dir + filename)
    return filename


def combine_bg(result, bg_file, text, x=0, y=0):
    save_dir = 'static/image/'
    now = datetime.now()
    bg_file.paste(result, (x, y), result)
    filename = "cb_" + text + now.strftime("_%m_%d_%Y_%H_%M_%S.png")
    bg_file.save(save_dir + filename)
    com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
    os.system(com)
    return filename
