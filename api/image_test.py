import tensorflow as tf
import numpy as np
import infogan
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cv2

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

sess = tf.compat.v1.Session()
model = infogan.GAN(sess)
save_dir = "./infogan_model/type1/"
filename = "type1_1.ckpt"
model.saver.restore(sess, save_dir+filename)
noise = np.full((1, 62), 0)
noise = np.tile(noise, [1, 1])
latent_code = np.zeros([1, 4])

generated = sess.run(model.Gen, {
            model.noise_source: noise, model.latent_code: latent_code, model.is_train: False
        })
img = np.reshape(generated, (model.height, model.width))  # 이미지 형태로. #num_generate, height, width

#img = blur(img)
#img = remove_noise(img)

fig = plt.figure(figsize=(1, 1))
gs = gridspec.GridSpec(1, 1)
gs.update(wspace=0.05, hspace=0.05)
ax = plt.subplot(gs[0])
plt.axis('off')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_aspect('equal')
plt.imshow(img, cmap='Greys_r')
plt.show()
plt.close(fig)