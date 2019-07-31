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
    fig = plt.figure(figsize=(4, 4))
    gs = gridspec.GridSpec(4, 4)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28, 28), cmap='Greys_r')

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

sess_a = tf.Session()
sess_a.run(tf.global_variables_initializer())

sess_b = tf.Session()
sess_b.run(tf.global_variables_initializer())

saver_a = tf.train.Saver()
saver_b = tf.train.Saver()
# saver_c=tf.train.Saver()
# saver_d=tf.train.Saver()
# saver_e=tf.train.Saver()


model_dir = './model/'
saver_a.restore(sess_a, model_dir + 'A/A.ckpt')
saver_b.restore(sess_b, model_dir + 'B/B.ckpt')
# saver_c.restore(sess, model_dir+'C/C.ckpt')
# saver_d.restore(sess, model_dir+'D/D.ckpt')
# saver_e.restore(sess, model_dir+'E/E.ckpt')

z_a = ""
z_b = ""
z_c = ""
z_d = ""
z_e = ""

with open("./z_value/A.txt", "r") as f:
    z_a = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ")
with open("./z_value/B.txt", "r") as f:
    z_b = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
with open("./z_value/C.txt", "r") as f:
    z_c = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ")
with open("./z_value/D.txt", "r") as f:
    z_d = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ")
with open("./z_value/E.txt", "r") as f:
    z_e = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ")

z_a = z_a[1:]
z_a = z_a[:-1]
z_a = z_a.split(" ")
z_a = [float(f) for f in z_a]
z_a = np.array(z_a)
z_a = z_a.reshape(16, 100)

z_b = z_b[1:]
z_b = z_b[:-1]
z_b = z_b.split(" ")
z_b = [float(f) for f in z_b]
z_b = np.array(z_b)
z_b = z_b.reshape(16, 100)

z_c = z_c[1:]
z_c = z_c[:-1]
z_c = z_c.split(" ")
z_c = [float(f) for f in z_c]
z_c = np.array(z_c)
z_c = z_c.reshape(16, 100)

z_d = z_d[1:]
z_d = z_d[:-1]
z_d = z_d.split(" ")
z_d = [float(f) for f in z_d]
z_d = np.array(z_d)
z_d = z_d.reshape(16, 100)

z_e = z_e[1:]
z_e = z_e[:-1]
z_e = z_e.split(" ")
z_e = [float(f) for f in z_e]
z_e = np.array(z_e)
z_e = z_e.reshape(16, 100)

y = np.zeros(shape=[16, y_dim])
y[:, np.random.randint(0, y_dim)] = 1.
'''print(z_a[0]-z_a[1])
tmp =np.zeros(100)
for i in z_a:
    tmp+=i
z_a[0] = tmp[8:]/16'''
samples = sess_a.run(X_samples, feed_dict={z: z_a, c: y})

fig = plot(samples)
plt.show()
plt.close(fig)

'''samples = sess_b.run(X_samples, feed_dict={z: z_b, c: y})
fig = plot(samples)
plt.show()
plt.close(fig)'''
