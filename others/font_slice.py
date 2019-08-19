from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import glob
import cv2
import os
images = glob.glob('./img/14/*.png')
print(images)

for idx, i in enumerate(images):
    tmp = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
    tmp = tmp[20:48, :]
    plt.imsave('./img/15/{}.png'.format(idx), tmp)

#data[12, 12] = [0]
'''img = Image.fromarray(data, '1')
img.show()

img2 = Image.fromarray(data2,'1')
img2.show()'''