from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


import cv2


random_image = np.random.random([500,500])

filename = './1.PNG'
filename2 = './2.PNG'

tmp = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
tmp2 = cv2.imread(filename2, cv2.IMREAD_GRAYSCALE)

# 붙지 않은 '가'
result = np.zeros((28,56))
result[:,:28] = tmp
result[:,28:] = tmp2
plt.imsave("a.png",result)

# 'ㅏ' 가 덮어버린 '가'
result = np.zeros((28,40))
result[:,:28] = tmp
result[:,12:] = tmp2
plt.imsave("b.png",result)
print(result)


result = np.zeros((28,46))
result.fill(255)
result[:,:28] = tmp
for idx_i, val_i in enumerate(tmp2):
	for idx_j, val_j in enumerate(val_i):
		if tmp2[idx_i,idx_j]<result[idx_i,idx_j+18]:
			result[idx_i,idx_j+18] = tmp2[idx_i,idx_j]
			print(tmp2[idx_i,idx_j])


plt.imsave("c.png",result)

#data[12, 12] = [0]
'''img = Image.fromarray(data, '1')
img.show()

img2 = Image.fromarray(data2,'1')
img2.show()'''