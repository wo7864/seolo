import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import sys
import os
sys.setrecursionlimit(1000000)


def rgba2rgb(filename):
    png = Image.open('font/PNG/'+filename+'.png')
    png.load()  # required for png.split()

    background = Image.new("RGB", png.size, (255, 255, 255))
    background.paste(png, mask=png.split()[3])  # 3 is the alpha channel

    background.save('font/JPG/'+filename+'.jpg', 'JPEG', quality=80)

# 현재 떨림체는 변환 문제로 제외한 상태
'''
font_list = ['bangwool', 'bangwool_b', 'baram', 'baram_b', 'bawi', 'bawi_b', 'bburi', 'bidan', 'bidan_b', 'bori',
             'bori_b', 'buddle', 'buddle_b', 'dasle', 'goorm', 'groom_b', 'jandi', 'janggun', 'namu',
             'namu_b', 'namu_c', 'sandle', 'seassack', 'seassack_b', 'sonmut', 'sonmut_b', 'taepoong', 'yetdol']
'''
font_list = ['yuwool']
'''
for i in font_list:
    rgba2rgb(i)
'''


def search(row, col, img, visit, row_value, col_value):
    visit[row][col] = 1
    row_value.append(row)
    col_value.append(col)
    num = [2]
    for i in num:
        if row != 0+i-1 and img[row-i][col] <= 200 and visit[row-i][col] == 0:
            search(row-i, col, img, visit, row_value, col_value)
        if row != 3334-i and img[row+i][col] <= 200 and visit[row+i][col] == 0:
            search(row+i, col, img, visit, row_value, col_value)
        if col != 0+i-1 and img[row][col-i] <= 200 and visit[row][col-i] == 0:
            search(row, col-i, img, visit, row_value, col_value)
        if col != 5001-i and img[row][col+i] <= 200 and visit[row][col+i] == 0:
            search(row, col+i, img, visit, row_value, col_value)
    return 0


def search2(row_value, col_value, img, visit):
    num = 10
    for i in range(len(row_value)):
        if img[row_value[i]+num][col_value[i]] <= 200:
            search(row_value[i]+num, col_value[i], img, visit, row_value, col_value)
        if img[row_value[i]-num][col_value[i]] <= 200:
            search(row_value[i]-num, col_value[i], img, visit, row_value, col_value)
        if img[row_value[i]][col_value[i]+num] <= 200:
            search(row_value[i], col_value[i]+num, img, visit, row_value, col_value)
        if img[row_value[i]][col_value[i]-num] <= 200:
            search(row_value[i], col_value[i]-num, img, visit, row_value, col_value)


for filename in font_list:
    img = cv2.imread('font/JPG/{}.jpg'.format(filename), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img[0:216, 167:305] = 255
    img[0:216, 2542:2680] = 255
    img[182:3124, 150:314] = 255
    img[182:2700, 2533:2691] = 255
    img[2983:3215, 2700:4264] = 255

    visit = np.zeros([3333, 5000])
    data = []
    height_line = [120, 360, 580, 800, 1020, 1240, 1460, 1660, 1880, 2100, 2320, 2540, 2760, 2980, 3200]
    for k in range(1, len(height_line)):
        col = 0
        while col < 2500:
            row = height_line[k-1]
            while row < height_line[k]:
                if img[row][col] <= 100 and visit[row][col] == 0:
                    row_value = []
                    col_value = []
                    search(row, col, img, visit, row_value, col_value)
                    search2(row_value, col_value, img, visit)
                    edge = [max(row_value)+5, min(row_value)-5, max(col_value)+5, min(col_value)-5]
                    data.append(edge)
                    visit[edge[1]:edge[0], edge[3]:edge[2]] = 1
                row += 1
            col += 1
    for k in range(1, len(height_line)):
        col = 2500
        while col < 5000:
            row = height_line[k-1]
            while row < height_line[k]:
                if img[row][col] <= 100 and visit[row][col] == 0:
                    row_value = []
                    col_value = []
                    search(row, col, img, visit, row_value, col_value)
                    search2(row_value, col_value, img, visit)
                    edge = [max(row_value)+5, min(row_value)-5, max(col_value)+5, min(col_value)-5]
                    data.append(edge)
                    visit[edge[1]:edge[0], edge[3]:edge[2]] = 1
                row += 1
            col += 1

    for idx, i in enumerate(data):
        try:
            tmp = img[i[1]:i[0], i[3]:i[2]]
            height, width = tmp.shape[:2]
            if height > width:
                share = 128 / height
                width = int(share * width)
                if height > 128:
                    tmp = cv2.resize(tmp, (width, 128), interpolation=cv2.INTER_LINEAR)
                else:
                    tmp = cv2.resize(tmp, (width, 128), interpolation=cv2.INTER_AREA)
                tmp2 = np.full([128, int((128-width) / 2)], 255)
                tmp3 = np.full([128, 128-(width + tmp2.shape[1])], 255)
                tmp = np.hstack([tmp2, tmp])
                tmp = np.hstack([tmp, tmp3])
            else:
                share = 128 / width
                height = int(share * height)
                if width > 128:
                    tmp = cv2.resize(tmp, (128, height), interpolation=cv2.INTER_LINEAR)
                else:
                    tmp = cv2.resize(tmp, (128, height), interpolation=cv2.INTER_AREA)
                tmp2 = np.full([int((128-height) / 2), 128], 255)
                tmp3 = np.full([128-(height + tmp2.shape[0]), 128], 255)
                tmp = np.vstack([tmp2, tmp])
                tmp = np.vstack([tmp, tmp3])
            plt.imsave('font/{}/{}.png'.format(filename, str(idx)), tmp, cmap='Greys_r')
        except Exception as e:
            print(str(e))