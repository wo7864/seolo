import os
import cv2
import numpy as np

for i in range(1, 27):
    data_list = []
    data_dir = 'C://Users/wo786/dcgan_test/font/seassack_b/'+str(i)
    file_list = os.listdir(data_dir)
    for f in file_list:
        img = cv2.imread(data_dir + '/{}'.format(f), cv2.IMREAD_GRAYSCALE)
        img = np.array(img).reshape(28, 28, 1)
        data_list.append(img)
    file_name = 'type5_{}.npy'.format(str(i))
    np.save('./npy/{}'.format(file_name), data_list)
