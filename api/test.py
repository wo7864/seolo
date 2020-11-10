
import test_main
import load_model

import numpy as np
import cv2
import os
from urllib import parse
import json
import werkzeug
from PIL import Image
from werkzeug.datastructures import FileStorage
import io
from PIL import Image
phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
    , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']


param_list = [50] * 4
blur = 0
color = '000000'
is_invisiable = 'False'
input_text = '안녕'
text, shape_list = test_main.convert_text(input_text)
latter_list, json_latter_list = test_main.create_latter_list(0, text, shape_list)
filename, _, image_width, image_height = test_main.img_attach(latter_list, blur, color, is_invisiable, input_text, None)


