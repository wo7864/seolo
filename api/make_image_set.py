import tensorflow as tf
import infogan
import numpy as np
from PIL import Image
import main
import os


def gen_image(model, sess, param_list):
    noise = np.random.uniform(-1.0, 1.0, size=[1, 50])
    latent_code = param_list
    generated = sess.run(model.Gen, {  # num_generate, 28, 28, 1
        model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
    }
    )
    img = np.reshape(generated, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width
    return img


font = 'type8'
phoneme = 1
tf.reset_default_graph()
sess = tf.compat.v1.Session()
model = infogan.GAN()
model_dir = "./infogan_model/{}/".format(font)
filename = "{}_{}.ckpt".format(font, phoneme)
model.saver.restore(sess, model_dir+filename)

save_dir = "./static/image/{}/{}/".format(font, phoneme)

if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

shape = 0
if not os.path.isdir(save_dir + str(shape)):
    os.mkdir(save_dir + str(shape))
for i in range(-10, 11, 5):
    for j in range(-10, 11, 5):
        param_list = [[i/10, j/10, 0]]
        img = gen_image(model, sess, param_list)

        img = main.normalization(img)
        img = main.blur(img)
        img = main.set_definition(img)

        img = img[:] * 255
        result = Image.fromarray(img).convert('RGB')
        savename = "{}_{}_{}_{}_{}.png".format(font, phoneme, shape, i/10, j/10)
        result.save('./static/image/{}/{}/{}/{}'.format(font, phoneme, shape, savename))

