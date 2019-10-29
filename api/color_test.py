import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image



def show_image(img):
    fig = plt.figure(figsize=(1, 1))
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.05, hspace=0.05)
    plt.axis('off')
    plt.imshow(img, cmap='Greys_r')
    plt.show()
    plt.close(fig)


def set_color(result, r, g, b):
    r = np.full([result.shape[0], result.shape[1]], r)
    g = np.full([result.shape[0], result.shape[1]], g)
    b = np.full([result.shape[0], result.shape[1]], b)
    r = r[:] / 1
    g = g[:] / 1
    b = b[:] / 1
    result = 1 - result[:]
    result = result[:] * 255
    result = cv2.merge((r, g, b, result))
    result = result.astype(np.uint8)
    result = Image.fromarray(result, 'RGBA')
    return result


img = cv2.imread("test.png", cv2.IMREAD_GRAYSCALE)
img = img[:]/255
img2 = set_color(img, 16, 20, 0)
img3 = Image.open("bg_test.jpg").convert('RGBA').resize((img2.size[0], img2.size[1]))
img4 = img3
img3.paste(img2, (0, 0), img2)
img3.save("test2.png")

img2 = set_color(img, 16, 150, 200)
img4.paste(img2, (100, 0), img2)
img4.save("test3.png")
