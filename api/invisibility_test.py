import numpy as np
import cv2

def set_invisibility(result, color):
    tmp = np.full([result.shape[0], result.shape[1]], 1.0)
    for idx, i in enumerate(result):
        for idx2, j in enumerate(i):
            if color == 0:
                if j == 1:
                    tmp[idx][idx2] = 1 - j
            else:
                if j == -1:
                    tmp[idx][idx2] = 1 + j

    result = cv2.merge((result, result, result, tmp))
    return result
