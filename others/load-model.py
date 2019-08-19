import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import cv2

z_dim = 100
X_dim = 784
y_dim = 1
h_dim = 128
c = 0
lr = 1e-3

'''def plot(samples):
    fig = plt.figure(figsize=(1, 1))
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):
        if i == 0:
            ax = plt.subplot(gs[i])
            plt.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_aspect('equal')
            plt.imshow(sample.reshape(28, 28), cmap='Greys_r')

    return fig'''


def plot(samples):
    fig = plt.figure(figsize=(1, len(samples)))
    gs = gridspec.GridSpec(1, len(samples))
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28, 28), cmap='Greys_r')

    return fig

def img_attach(samples):
    img_size = 28
    attach = 16  # 이미지를 붙이는 정도. 작을수록 글자 간의 간격이 좁아진다.
    width = attach*(len(samples)-1)+img_size
    result = np.zeros((img_size, width))
    result.fill(1)
    for idx, img in enumerate(samples):
        img = img.reshape(img_size, img_size)
        if idx==0:
            result[:,:img_size] = img
        else:
            for idx_i, val_i in enumerate(img):
                for idx_j, val_j in enumerate(val_i):
                    if img[idx_i, idx_j] < result[idx_i, attach*idx + idx_j]:
                        result[idx_i, attach*idx + idx_j] = img[idx_i, idx_j]

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

def xavier_init(size):
    in_dim = size[0]
    xavier_stddev = 1. / tf.sqrt(in_dim / 2.)
    return tf.random_normal(shape=size, stddev=xavier_stddev)


# =============================== Q(z|X) ======================================

X = tf.placeholder(tf.float32, shape=[None, X_dim])
c = tf.placeholder(tf.float32, shape=[None, y_dim])
z = tf.placeholder(tf.float32, shape=[None, z_dim])

Q_W1 = tf.Variable(xavier_init([X_dim + y_dim, h_dim]))
Q_b1 = tf.Variable(tf.zeros(shape=[h_dim]))

Q_W2_mu = tf.Variable(xavier_init([h_dim, z_dim]))
Q_b2_mu = tf.Variable(tf.zeros(shape=[z_dim]))

Q_W2_sigma = tf.Variable(xavier_init([h_dim, z_dim]))
Q_b2_sigma = tf.Variable(tf.zeros(shape=[z_dim]))


def Q(X, c):
    inputs = tf.concat(axis=1, values=[X, c])
    h = tf.nn.relu(tf.matmul(inputs, Q_W1) + Q_b1)
    z_mu = tf.matmul(h, Q_W2_mu) + Q_b2_mu
    z_logvar = tf.matmul(h, Q_W2_sigma) + Q_b2_sigma
    return z_mu, z_logvar


def sample_z(mu, log_var):
    eps = tf.random_normal(shape=tf.shape(mu))
    return mu + tf.exp(log_var / 2) * eps


# =============================== P(X|z) ======================================

P_W1 = tf.Variable(xavier_init([z_dim + y_dim, h_dim]))
P_b1 = tf.Variable(tf.zeros(shape=[h_dim]))

P_W2 = tf.Variable(xavier_init([h_dim, X_dim]))
P_b2 = tf.Variable(tf.zeros(shape=[X_dim]))


def P(z, c):
    inputs = tf.concat(axis=1, values=[z, c])
    h = tf.nn.relu(tf.matmul(inputs, P_W1) + P_b1)
    logits = tf.matmul(h, P_W2) + P_b2
    prob = tf.nn.sigmoid(logits)
    return prob, logits


# =============================== TRAINING ====================================
# z_mu, z_logvar = Q(X, c)
# z_sample = sample_z(z_mu, z_logvar)
# _, logits = P(z_sample, c)


# E[log P(X|z)]
# recon_loss = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=X), 1)
# D_KL(Q(z|X) || P(z|X)); calculate in closed form as both dist. are Gaussian
# kl_loss = 0.5 * tf.reduce_sum(tf.exp(z_logvar) + z_mu**2 - 1. - z_logvar, 1)
# VAE loss
# vae_loss = tf.reduce_mean(recon_loss + kl_loss)
# solver = tf.train.AdamOptimizer().minimize(vae_loss)


# Sampling from random z

X_samples, _ = P(z, c)

model_dir = './model/'
sess_list = []
saver_list = []
model_list = ['A', 'B', 'C', 'D', 'E']
z_list = []

for i in range(5):
    sess_list.append(tf.Session())
    saver_list.append(tf.train.Saver())

for idx, sess in enumerate(sess_list):
    sess.run(tf.global_variables_initializer())
    saver_list[idx].restore(sess, model_dir + '{}/{}.ckpt'.format(model_list[idx], model_list[idx]))
    with open("./z_value/{}.txt".format(model_list[idx]), "r") as f:
        z_value = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
        z_value = z_value[1:-1].split(" ")
        z_value = [float(f) for f in z_value]
        z_value = np.array(z_value).reshape(16,100)
        z_list.append(z_value)

'''tmp =np.zeros(100)
for i in z_a:
    tmp+=i
z_a[0] = tmp[:]/32'''


# z값 그래프로 찍어보기
'''y1_value = z_a[1]*100
x_name=[i for i in range(100)]
n_groups = len(x_name)
index = np.arange(n_groups)

plt.bar(index, y1_value, tick_label=x_name, align='center')

plt.xlabel('month')
plt.ylabel('average rainfall (mm)')
plt.title('Weather Bar Chart')
plt.xlim( -1, n_groups)
plt.ylim( 0, 100)
plt.show()
'''

y = np.zeros(shape=[1, y_dim])
y[:, np.random.randint(0, y_dim)] = 1.

samples = []
a = input()
from random import *

for i in a:
    rand_num = randint(0, 15)
    if i=="a":
        samples.append(sess_list[0].run(X_samples, feed_dict={z: z_list[0][rand_num].reshape(1,100), c: y}))
    elif i=="b":
        samples.append(sess_list[1].run(X_samples, feed_dict={z: z_list[1][rand_num].reshape(1,100), c: y}))
    elif i=="c":
        samples.append(sess_list[2].run(X_samples, feed_dict={z: z_list[2][rand_num].reshape(1,100), c: y}))
    elif i=="d":
        samples.append(sess_list[3].run(X_samples, feed_dict={z: z_list[3][rand_num].reshape(1,100), c: y}))
    elif i=="e":
        samples.append(sess_list[4].run(X_samples, feed_dict={z: z_list[4][rand_num].reshape(1,100), c: y}))

test = img_attach(samples)
plt.show()
#fig = plot(samples)
#plt.show()
plt.close(test)

'''samples = sess_b.run(X_samples, feed_dict={z: z_b, c: y})
fig = plot(samples)
plt.show()
plt.close(fig)'''
