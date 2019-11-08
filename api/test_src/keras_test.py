import tensorflow as tf
import numpy as np
import infogan as infogan
import cv2
from PIL import Image
from keras.models import model_from_json
from keras.models import Model
from keras.layers.core import Flatten, Dense, Dropout, Activation, Lambda, Reshape
from keras.layers.convolutional import Conv2D, Deconv2D, ZeroPadding2D, UpSampling2D
from keras.layers import Input, Concatenate
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D
import keras.backend as K


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
    result = result[:] - min_value
    max_value = np.max(result)
    result = result[:] / max_value
    return result


def set_definition(result, definition=80):
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


def generator_deconv(cont_dim, noise_dim, img_dim, bn_mode, batch_size, model_name="generator_deconv", dset="mnist"):

    assert K.backend() == "tensorflow", "Deconv not implemented with theano"

    s = img_dim[1]
    f = 128

    if dset == "mnist":
        start_dim = int(s / 4)
        nb_upconv = 2
    else:
        start_dim = int(s / 16)
        nb_upconv = 4

    reshape_shape = (start_dim, start_dim, f)
    bn_axis = -1
    output_channels = img_dim[-1]

    cont_input = Input(shape=cont_dim, name="cont_input")
    noise_input = Input(shape=noise_dim, name="noise_input")

    gen_input = Concatenate()([cont_input, noise_input])

    x = Dense(1024)(gen_input)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    x = Dense(f * start_dim * start_dim)(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    x = Reshape(reshape_shape)(x)

    # Transposed conv blocks
    for i in range(nb_upconv - 1):
        nb_filters = int(f / (2 ** (i + 1)))
        s = start_dim * (2 ** (i + 1))
        o_shape = (batch_size, s, s, nb_filters)
        x = Deconv2D(nb_filters, (3, 3), output_shape=o_shape, strides=(2, 2), padding="same")(x)
        x = BatchNormalization(axis=bn_axis)(x)
        x = Activation("relu")(x)

    # Last block
    s = start_dim * (2 ** (nb_upconv))
    o_shape = (batch_size, s, s, output_channels)
    x = Deconv2D(output_channels, (3, 3), output_shape=o_shape, strides=(2, 2), padding="same")(x)
    x = Activation("tanh")(x)

    generator_model = Model(inputs=[cont_input, noise_input], outputs=[x], name=model_name)

    return generator_model


def load(cont_dim, noise_dim, img_dim, bn_mode, batch_size, dset="mnist", use_mbd=False):
    model = generator_deconv(cont_dim, noise_dim, img_dim, bn_mode, batch_size, model_name="generator_deconv", dset=dset)
    model.summary()
    return model

cont_dim = (2,)
noise_dim = (64,)
img_dim = (4000, 64, 64, 1)
bn_mode = 2
batch_size = 32


model = load(cont_dim, noise_dim, img_dim, bn_mode, batch_size)
model.load_weights("./infogan_model/gen_weights_epoch10.h5")

X_noise = np.random.normal(scale=1.0, size=(batch_size, noise_dim[0]))
X_cont = np.random.normal(scale=1.0, size=(batch_size, noise_dim[0]))
X_cont = np.repeat(X_cont[:1, :], batch_size, axis=0)  # fix continuous noise

img = None
img = np.reshape(img, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width

img = normalization(img)
#img = blur(img)
#img = set_definition(img)

img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_LINEAR)
#img = update_rotation(img, 0)
img = set_color_rgb(img)

img.save("test.png")
