#https://arxiv.org/abs/1606.03657

import tensorflow as tf #version 1.4
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.compat.v1.keras.utils import plot_model
from tensorflow.examples.tutorials.mnist import input_data
import os

class GAN:

	def __init__(self, sess):
		self.train_rate_D_Q = 0.0002
		self.train_rate_G = 0.001
		self.channel = 1 #mnist는 흑백
		self.height = 64 #mnist 28*28인데 resize 해줘서 64*64임.
		self.width = 64
		self.noise_dim = 50 # 노이즈 차원 #infogan paper
		self.continuous = 3


		with tf.name_scope("placeholder"):
			#class 밖에서 모델 실행시킬때 학습데이터 넣어주는곳.
			self.X = tf.placeholder(tf.float32, [None, self.height, self.width, self.channel])
			
			#class 밖에서 모델 실행시킬때 class의 Generate_noise 실행한 결과를 넣어주는 곳.
			self.noise_source = tf.placeholder(tf.float32, [None, self.noise_dim])
	
			#class 밖에서 모델 실행시킬때 class의 Generate_latent_code 실행한 결과를 넣어주는 곳.
			self.latent_code = tf.placeholder(tf.float32, [None, self.continuous])

			#batch_norm
			self.is_train = tf.placeholder(tf.bool)
		


		#노이즈로 데이터 생성. 
		with tf.name_scope("generate_image_from_noise"):
			self.Gen = self.Generator(self.noise_source, self.latent_code) #batch_size, self.height, self.width, self.channel



		#Discriminator가 진짜라고 생각하는 확률		
		with tf.name_scope("result_from_Discriminator"):
			#학습데이터가 진짜일 확률
			self.D_X, self.D_X_logits = self.Discriminator(self.X) #batch_size, 1, 1, 1
			#G(noise,latent_code)로부터 생성된 데이터가 진짜일 확률, G(noise,latent_code)로부터 재생성한 latent_code들(discrete_c, continuous_c). 
			self.D_Gen, self.D_Gen_logits, self.continuous_c = self.Discriminator(self.Gen, True)



		with tf.name_scope("loss"):
			#Discriminator 입장에서 최소화 해야 하는 값
			self.D_loss = self.Discriminator_loss_function(self.D_X_logits, self.D_Gen_logits)
			#Generator 입장에서 최소화 해야 하는 값.
			self.G_loss = self.Generator_loss_function(self.D_Gen_logits)
			#Q 입장에서 최소화 해야 하는 값.
			self.Q_loss = self.Q_loss_function(self.latent_code, self.continuous_c)


		#학습 코드
		with tf.name_scope("train"):
			#Batch norm 학습 방법 : https://www.tensorflow.org/versions/r1.4/api_docs/python/tf/layers/batch_normalization
			with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
					
					#Discriminator와 Generator, Q에서 사용된 variable 분리.
				self.D_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = 'Discriminator')
				self.G_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = 'Generator')
				self.Q_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = 'Q')
					
				self.D_minimize = tf.train.AdamOptimizer(
							learning_rate=self.train_rate_D_Q, beta1=0.5).minimize(self.D_loss, var_list=self.D_variables) #D 변수만 학습.
				self.G_minimize = tf.train.AdamOptimizer(
							learning_rate=self.train_rate_G, beta1=0.5).minimize(self.G_loss, var_list=self.G_variables) #G 변수만 학습.
				self.Q_minimize = tf.train.AdamOptimizer(
							learning_rate=self.train_rate_D_Q, beta1=0.5).minimize(self.Q_loss, var_list=[self.G_variables, self.Q_variables]) #G, Q 변수만 학습.



		#tensorboard
		with tf.name_scope("tensorboard"):
			self.D_loss_tensorboard = tf.placeholder(tf.float32) #Discriminator 입장에서 최소화 해야 하는 값
			self.G_loss_tensorboard = tf.placeholder(tf.float32) #Generator 입장에서 최소화 해야 하는 값.
			self.Q_loss_tensorboard = tf.placeholder(tf.float32) #Q 입장에서 최소화 해야 하는 값. Reconstruction Loss

			self.D_loss_summary = tf.summary.scalar("D_loss", self.D_loss_tensorboard) 
			self.G_loss_summary = tf.summary.scalar("G_loss", self.G_loss_tensorboard) 
			self.Q_loss_summary = tf.summary.scalar("Q_loss", self.Q_loss_tensorboard) 
			
			self.merged = tf.summary.merge_all()
			self.writer = tf.summary.FileWriter('./tensorboard/', sess.graph)



		with tf.name_scope("saver"):
			self.saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="Generator"))

		sess.run(tf.global_variables_initializer())



	#노이즈 생성
	def Generate_noise(self, batch_size): #batch_size, 1, 1, self.noise_dim
		return np.random.uniform(-1.0, 1.0, size=[batch_size, self.noise_dim]) #-1~1의 uniform distribution DCGAN논문에서 나온대로.



	#latent code c 생성
	def Generate_latent_code(self, batch_size):
		#https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.random.uniform.html
		continuous_c = np.random.uniform(-1, 1, [batch_size, self.continuous]) # batch, self.continuous
		return continuous_c



	#데이터의 진짜일 확률 InfoGAN paper
	def Discriminator(self, data, reuse=False): #batch_size, 1, 1, 1
		with tf.variable_scope('Discriminator') as scope:
			if reuse == True: #Descriminator 함수 두번 부르는데 두번째 부르는 때에 같은 weight를 사용하려고 함.
				scope.reuse_variables()

			#input layer는 BN 안함.
			D_conv1 = tf.layers.conv2d(inputs=data, filters=64, kernel_size=[4, 4], strides=(2, 2), padding='same') #batch, 14, 14, 64
			D_conv1 = tf.nn.leaky_relu(D_conv1) # default leak is 0.2
			
			D_conv2 = tf.layers.conv2d(inputs=D_conv1, filters=128, kernel_size=[4, 4], strides=(2, 2), padding='same') #batch, 7, 7, 128
			D_conv2 = tf.layers.batch_normalization(D_conv2, training=self.is_train)
			D_conv2 = tf.nn.leaky_relu(D_conv2)
			
			flatten = tf.layers.flatten(D_conv2)
			D_fc1 = tf.layers.dense(flatten, 512, activation=None) #batch, 1024
			D_fc1 = tf.layers.batch_normalization(D_fc1, training=self.is_train)
			D_fc1 = tf.nn.leaky_relu(D_fc1)
			
			D_fc2_logits = tf.layers.dense(D_fc1, 1, activation=None) #batch, 1
			D_fc2_P = tf.nn.sigmoid(D_fc2_logits)
			

		# Q 연산부분 C를 Reconstruction 하는 부분임.
		if reuse == True: 
			with tf.variable_scope('Q'):
				#Q 연산부분.
				D_fc2_Q = tf.layers.dense(D_fc1, 128, activation=None) #batch, 128
				D_fc2_Q = tf.layers.batch_normalization(D_fc2_Q, training=self.is_train)
				D_fc2_Q = tf.nn.leaky_relu(D_fc2_Q)

				D_fc3_Q = tf.layers.dense(D_fc2_Q, self.continuous, activation=None) #batch, self.categorical+self.continuous
				continuous_c = D_fc3_Q[:, :]

			return D_fc2_P, D_fc2_logits, continuous_c

		else: 
			return D_fc2_P, D_fc2_logits


	#노이즈로 진짜같은 데이터 생성 InfoGAN paper
	def Generator(self, noise, latent_code): #batch_size, self.height, self.width, self.channel
		#concat noise || latent_code
		noise_c = tf.concat((noise, latent_code), axis=-1) #batch, self.noise_dim+self.categorical+self.continuous

		with tf.variable_scope('Generator'):
			#project and reshape 논문 부분.
			G_fc1 = tf.layers.dense(noise_c, 512, activation=None, name='G_fc1')
			G_fc1 = tf.layers.batch_normalization(G_fc1, training=self.is_train, name='G_fc1_bn')
			G_fc1 = tf.nn.relu(G_fc1)

			G_fc2 = tf.layers.dense(G_fc1, 16*16*128, activation=None, name='G_fc2')
			G_fc2 = tf.layers.batch_normalization(G_fc2, training=self.is_train, name='G_fc2_bn')
			G_fc2 = tf.nn.relu(G_fc2)
			G_fc2 = tf.reshape(G_fc2, [-1, 16, 16, 128])

			G_upconv1 = tf.layers.conv2d_transpose(inputs=G_fc2, filters=64, kernel_size=[4, 4], strides=(2, 2), padding='same') #batch, 14, 14, 64
			G_upconv1 = tf.layers.batch_normalization(G_upconv1, training=self.is_train, name='G_upconv1_bn')
			G_upconv1 = tf.nn.relu(G_upconv1)

			G_upconv2 = tf.layers.conv2d_transpose(inputs=G_upconv1, filters=self.channel, kernel_size=[4, 4], strides=(2, 2), padding='same') # batch, 28, 28, 1
	
			return G_upconv2

	
	#Discriminator 학습.
	def Discriminator_loss_function(self, D_X_logits, D_Gen_logits):
		#return tf.reduce_mean(tf.log(D_X) + tf.log(1-D_Gen)) 기존 코드.		
		#위 식이 최대화가 되려면 D_X가 1이 되어야 하며, D_Gen이 0이 되어야 한다.
		#tf.ones_like(X) X와 같은 shape의 1로 이루어진 tensor를 리턴. D_X_logits을 sigmoid 한 결과와 1의 오차.
		D_X_loss = tf.nn.sigmoid_cross_entropy_with_logits(
					labels=tf.ones_like(D_X_logits), 
					logits=D_X_logits
				)

		D_Gen_loss = tf.nn.sigmoid_cross_entropy_with_logits(
					labels=tf.zeros_like(D_Gen_logits),
					logits=D_Gen_logits
				)

		#이 두 오차의 합을 최소화 하도록 학습.
		D_loss = tf.reduce_mean(D_X_loss) + tf.reduce_mean(D_Gen_loss)

		return D_loss


 
	#Generator 입장에서 최소화 해야 하는 값.
	def Generator_loss_function(self, D_Gen_logits):
		#return tf.reduce_mean(tf.log(D_Gen))
		#위 식이 최대화가 되려면 D_Gen이 1이 되어야 함. == 1과의 차이를 최소화 하도록 학습하면 됨.
		G_loss = tf.nn.sigmoid_cross_entropy_with_logits(
					labels=tf.ones_like(D_Gen_logits), 
					logits=D_Gen_logits
				)
		
		G_loss = tf.reduce_mean(G_loss) 

		return G_loss



	def Q_loss_function(self, latent_code, continuous_c):
		#원본 latent_code C와의 reconstruction loss임.



		#continus_loss는 기울어짐, 너비 를 배움. 이것은 원핫 표현이 아니므로 MSE loss 사용함.
		continuous_loss = tf.reduce_sum(tf.square(latent_code[:, :] - continuous_c), axis=-1)

		Q_loss = 0.5*tf.reduce_mean(continuous_loss)

		return Q_loss


def train(model, data):
	total_D_loss = 0
	total_G_loss = 0
	total_Q_loss = 0

	iteration = int(np.ceil(len(data)/batch_size))


	for i in range( iteration ):
		#train set. mini-batch
		input_ = data[batch_size * i: batch_size * (i + 1)]

		#노이즈 생성.
		noise = model.Generate_noise(len(input_))  # len(input_) == batch_size, noise = (batch_size, model.noise_dim)
		latent_code = model.Generate_latent_code(len(input_)) # (batch, self.categorical + self.continuous)
			
		#Discriminator 학습.
		_, D_loss = sess.run([model.D_minimize, model.D_loss], {
						model.X:input_, model.noise_source:noise, model.latent_code:latent_code, model.is_train:True
					}
				)
		
		#Generator 학습. 		#batch_normalization을 하기 때문에 X data도 넣어줘야함.
		_, G_loss = sess.run([model.G_minimize, model.G_loss], {
						model.X:input_, model.noise_source:noise, model.latent_code:latent_code, model.is_train:True
					}
				)
		
		#Q 학습.
		_, Q_loss = sess.run([model.Q_minimize, model.Q_loss], {
						model.X:input_, model.noise_source:noise, model.latent_code:latent_code, model.is_train:True
					}
				)
		

		#parameter sum
		total_D_loss += D_loss
		total_G_loss += G_loss
		total_Q_loss += Q_loss
	

	return total_D_loss/iteration, total_G_loss/iteration, total_Q_loss/iteration



def write_tensorboard(model, D_loss, G_loss, Q_loss, epoch):
	summary = sess.run(model.merged, 
					{
						model.D_loss_tensorboard:D_loss, 
						model.G_loss_tensorboard:G_loss,
						model.Q_loss_tensorboard:Q_loss,
					}
				)

	model.writer.add_summary(summary, epoch)


def run(font, phoneme, model, train_set, saver_path, restore = 0):
	#restore인지 체크.
	if restore != 0:
		model.saver.restore(sess, saver_path+str(restore)+".ckpt")
	
	print('training start')
	min_value = 100000
	#학습 진행
	for epoch in range(restore + 1, 201):
		np.random.shuffle(train_set)
		D_loss, G_loss, Q_loss = train(model, train_set)

		print("epoch : ", epoch, " D_loss : ", D_loss, " G_loss : ", G_loss, " Q_loss : ", Q_loss)
		
		if min_value >= Q_loss and Q_loss < 0.04:
			#tensorboard
			write_tensorboard(model, D_loss, G_loss, Q_loss, epoch)

			#weight 저장할 폴더 생성
			if not os.path.exists(saver_path):
				os.makedirs(saver_path)
			filename = font+'_'+str(phoneme)+".ckpt"
			save_path = model.saver.save(sess, saver_path+filename)
		
			#생성된 이미지 저장할 폴더 생성
			if not os.path.exists(make_image_path):
				os.makedirs(make_image_path)
			#gen_image(model, epoch)
			tf.train.write_graph(sess.graph_def, "./", "graph.pbtxt", as_text=True )


def copy_data(data):
  img_size = 64
  data = data.reshape(-1, img_size, img_size)
  np.random.shuffle(data)
  num = int(10/data.shape[0])

  tmp = [x / (num/40) for x in range(1, num)]
  rotation_gen_list = []
  for i in tmp:
    rotation_gen_list.append(ImageDataGenerator(shear_range=i, fill_mode='nearest'))

  img_cnt = data.shape[0]
  tmp_data = np.zeros((1, 64, 64))
  print(tmp_data.shape)
  for j in range(1):
    for rotation_gen in rotation_gen_list:
      it = rotation_gen.flow(data.reshape(img_cnt, img_size, img_size, 1), batch_size=img_cnt)
      for i in range(0, 1):
        gen_img = it.next()
        gen_img = gen_img.reshape(img_cnt, img_size, img_size)
        tmp_data = np.concatenate((tmp_data, gen_img), axis=0)
  data = np.concatenate((data, tmp_data[1:]), axis=0)
  #np.random.shuffle(data)

  img_cnt = data.shape[0]

  data = data.reshape(img_cnt, img_size, img_size, 1)
  data = data[:]/255
  print(data.shape)
  return data

font = 'type6'
phoneme_list = [x for x in range(1, 27)]
for i in phoneme_list:
  data = np.load('/content/gdrive/My Drive/Korean_model/npy/{}/{}_{}.npy'.format(font, font, str(i)))
  data = copy_data(data)

  saver_path = '/content/gdrive/My Drive/Korean_model/model/{}/'.format(font)
  make_image_path = '/content/gdrive/My Drive/Korean_model/model/generate/'

  batch_size = 128
  start_value = 2 #이미지 생성할때 continuous C 값을 -2~2 범위에서 변경하면서 생성하겠다는 의미임.

  tf.reset_default_graph ()
  sess = tf.Session()

  #model
  model = GAN(sess) 
  phoneme = i
  #run
  run(font, phoneme, model, data, saver_path)
