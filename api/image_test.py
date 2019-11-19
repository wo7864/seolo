import tensorflow as tf
import numpy as np
import infogan as infogan
import cv2
from PIL import Image
from keras.models import model_from_json


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


def remove_noise(img, size=4):
    width = img.shape[1]
    height = img.shape[0]
    degree = 0.6
    for x in range(width-size):
        for y in range(height-size):
            swi = 0
            for i in range(size+1):
                if not (img[y][x+i] > degree and img[y+size][x+i] > degree and img[y+i][x] > degree and img[y+i][x+size] > degree):
                    swi = 1
            if swi == 0:
                img[y+1:y+size][x+1:x+size] = 1
    return img


def set_color(result, color):
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



def set_color_rgba(result, color):
    r_color = int("0x" + color[:2], 16)
    g_color = int("0x" + color[2:4], 16)
    b_color = int("0x" + color[4:], 16)
    r = np.full([result.shape[0], result.shape[1]], r_color)
    g = np.full([result.shape[0], result.shape[1]], g_color)
    b = np.full([result.shape[0], result.shape[1]], b_color)
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

def normalization(result):
    min_value = np.min(result)
    max_value = np.max(result)
    if min_value < 0 or max_value > 1:
        result = result[:] - min_value
        max_value = np.max(result)
        result = result[:] / max_value
    return result


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


def update_rotation(img2, rotation):
    matrix = cv2.getRotationMatrix2D((img2.shape[1]/2, img2.shape[0]/2), rotation, 1)
    img2 = cv2.warpAffine(img2, matrix, (img2.shape[1], img2.shape[0]),  borderMode=cv2.BORDER_REPLICATE)
    return img2


sess = tf.compat.v1.Session()
model = infogan.GAN(sess)
save_dir = "./infogan_model/type8/"
filename = "type8_5.ckpt"
model.saver.restore(sess, save_dir+filename)
noise = np.full((1, 50), 0)
noise = np.tile(noise, [1, 1])
latent_code = np.full((1, 3), -1)

generated = sess.run(model.Gen, {
            model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
        })
img = np.reshape(generated, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width

img = normalization(img)
img = blur(img)
img = set_definition(img)
#img = blur(img)
#img = set_definition(img)
#img = cv2.blur(img, (i*2+1, i*2+1), 0)
img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_LINEAR)
#img = img.astype(np.uint8)
#img = Image.fromarray(img, 'L')
#img = update_rotation(img, 0)
img = set_color_rgba(img, "aaaaaa")

img.save("./test_img/test.png")
