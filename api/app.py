from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

import main
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

model_list, sess_list = load_model.load()
app = Flask(__name__)
CORS(app)

api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('font')
parser.add_argument('input_text')
parser.add_argument('latter_list')
parser.add_argument('latter_num')
parser.add_argument('phoneme_num')
parser.add_argument('blur')
parser.add_argument('image_height')
parser.add_argument('image_width')
parser.add_argument('is_invisiable')
parser.add_argument('color')
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
parser.add_argument('filename')
parser.add_argument('bg_filename')
parser.add_argument('x_in_bg')
parser.add_argument('y_in_bg')
phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
    , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']


class Calligraphy(Resource):

    def get(self):
        return 'hi'

    def post(self):
        args = parser.parse_args()
        font = int(args['font'])
        input_text = args['input_text']
        param_list = [50] * 4
        blur = 0
        color = '000000'
        is_invisiable = 'False'
        text, shape_list = main.convert_text(input_text)
        latter_list, json_latter_list = main.create_latter_list(font, model_list, sess_list, text, shape_list, param_list)
        filename, _, image_width, image_height = main.img_attach(latter_list, blur, color, is_invisiable, input_text, None)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "latter_list": json_latter_list,
            "filename": filename,
            "blur": blur,
            "color": color,
            "image_width": image_width,
            "image_height": image_height
        }
        return res
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        font = int(args['font'])
        latter_num = int(args['latter_num'])
        phoneme_num = int(args['phoneme_num'])
        input_text = args['input_text']
        blur = int(args['blur'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        color = args['color']
        is_invisiable = bool(args['is_invisiable'])
        bg_filename = args['bg_filename']
        bg_data = None
        if bg_filename:
            x_in_bg = int(args['x_in_bg'])
            y_in_bg = int(args['y_in_bg'])
            bg_data = (bg_filename, x_in_bg, y_in_bg)

        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        target = latter_list[latter_num][phoneme_num]
        model_num = phoneme_list.index(target.phoneme)
        target_img = main.gen_image(model_num, model_list[font][model_num],  sess_list[font][model_num], target.param_list)
        target_img = cv2.resize(target_img, (int(target.width), int(target.height)), interpolation=cv2.INTER_LINEAR)
        target_img = main.update_rotation(target_img, target.rotation)
        target.img = target_img
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, blur, color,
                                                                           is_invisiable, input_text, bg_data,
                                                                           image_width, image_height)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()

        target_img = main.gen_image(model_num, model_list[font][model_num],  sess_list[font][model_num], target.param_list)

        res = {
            "filename": filename,
            "cb_filename": cb_filename,
            "latter_list": text
        }
        return res


# 이미지 재생성
class PhonemeShapeOption(Resource):
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        font = int(args['font'])
        latter_num = int(args['latter_num'])
        phoneme_num = int(args['phoneme_num'])
        input_text = args['input_text']
        blur = int(args['blur'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        color = args['color']
        is_invisiable = args['is_invisiable']
        if is_invisiable == 'false':
            is_invisiable = False
        if is_invisiable == 'true':
            is_invisiable = True
        bg_filename = args['bg_filename']
        bg_data = None
        if bg_filename:
            x_in_bg = int(args['x_in_bg'])
            y_in_bg = int(args['y_in_bg'])
            bg_data = (bg_filename, x_in_bg, y_in_bg)

        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        target = latter_list[latter_num][phoneme_num]
        model_num = phoneme_list.index(target.phoneme)
        target_img = main.gen_image(model_num, model_list[font][model_num],  sess_list[font][model_num], target.param_list)
        target_img = cv2.resize(target_img, (int(target.width), int(target.height)), interpolation=cv2.INTER_LINEAR)
        target_img = main.update_rotation(target_img, target.rotation)
        target.img = target_img

        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, blur, color, is_invisiable, input_text, bg_data, image_width, image_height)

        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
            "cb_filename": cb_filename,
            "latter_list": text
        }
        return res


# 이미지 위치 조정
class PhonemeLocationOption(Resource):
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        input_text = args['input_text']
        color = args['color']
        blur = int(args['blur'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        is_invisiable = args['is_invisiable']
        if is_invisiable == 'false':
            is_invisiable = False
        if is_invisiable == 'true':
            is_invisiable = True
        bg_filename = args['bg_filename']
        bg_data = None
        if bg_filename:
            x_in_bg = int(args['x_in_bg'])
            y_in_bg = int(args['y_in_bg'])
            bg_data = (bg_filename, x_in_bg, y_in_bg)

        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, blur, color, is_invisiable, input_text, bg_data, image_width, image_height)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "filename": filename,
            "cb_filename": cb_filename,
            "latter_list": text
        }
        return res


# 이미지 크기 조정
class PhonemeSizeOption(Resource):
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        latter_num = int(args['latter_num'])
        phoneme_num = int(args['phoneme_num'])
        input_text = args['input_text']
        color = args['color']
        blur = int(args['blur'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        is_invisiable = args['is_invisiable']
        if is_invisiable == 'false':
            is_invisiable = False
        if is_invisiable == 'true':
            is_invisiable = True
        bg_filename = args['bg_filename']
        bg_data = None
        if bg_filename:
            x_in_bg = int(args['x_in_bg'])
            y_in_bg = int(args['y_in_bg'])
            bg_data = (bg_filename, x_in_bg, y_in_bg)

        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        target = latter_list[latter_num][phoneme_num]
        target.img = target.img.astype(np.uint8)
        target_img = cv2.resize(target.img, (int(target.width), int(target.height)), interpolation=cv2.INTER_LINEAR)
        latter_list[latter_num][phoneme_num].img = target_img
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, blur, color, is_invisiable, input_text, bg_data, image_width, image_height)

        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
            "cb_filename": cb_filename,
            "latter_list": text
        }
        return res


# 이미지 회전
class PhonemeRotationOption(Resource):
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        latter_num = int(args['latter_num'])
        phoneme_num = int(args['phoneme_num'])
        input_text = args['input_text']
        font = int(args['font'])
        color = args['color']
        blur = int(args['blur'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        is_invisiable = args['is_invisiable']
        if is_invisiable == 'false':
            is_invisiable = False
        if is_invisiable == 'true':
            is_invisiable = True
        bg_filename = args['bg_filename']
        bg_data = None
        if bg_filename:
            x_in_bg = int(args['x_in_bg'])
            y_in_bg = int(args['y_in_bg'])
            bg_data = (bg_filename, x_in_bg, y_in_bg)

        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        target = latter_list[latter_num][phoneme_num]
        model_num = phoneme_list.index(target.phoneme)
        target_img = main.gen_image(model_num, model_list[font][model_num],  sess_list[font][model_num], target.param_list)
        target_img = cv2.resize(target_img, (int(target.width), int(target.height)), interpolation=cv2.INTER_LINEAR)
        target_img = main.update_rotation(target_img, target.rotation)
        target.img = target_img
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, blur, color, is_invisiable, input_text, bg_data, image_width, image_height)

        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
            "cb_filename": cb_filename,
            "latter_list": text
        }
        return res


# 전체 이미지 옵션 수정
class ImageOption(Resource):
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        blur = int(args['blur'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        color = args['color']
        is_invisiable = args['is_invisiable']
        if is_invisiable == 'false':
            is_invisiable = False
        if is_invisiable == 'true':
            is_invisiable = True
        bg_filename = args['bg_filename']
        bg_data = None
        if bg_filename:
            x_in_bg = int(args['x_in_bg'])
            y_in_bg = int(args['y_in_bg'])
            bg_data = (bg_filename, x_in_bg, y_in_bg)

        input_text = args['input_text']
        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, blur, color, is_invisiable, input_text, bg_data, image_width, image_height)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "latter_list": text,
            "filename": filename,
            "cb_filename": cb_filename,
            "blur": blur,
            "color": color
        }
        return res


# 배경 합성하기
class AddBackGroundImage(Resource):
    def post(self):
        args = parser.parse_args()
        filename = args['filename']
        background_image = args['file']
        input_text = args['input_text']
        bg_filename = main.bg_file_save(background_image, input_text)
        save_dir = "./static/image/"
        img = Image.open(save_dir + filename)
        bg_img = Image.open(save_dir + bg_filename)
        filename = main.combine_bg(img, bg_img, input_text)

        res = {
            "bg_filename": bg_filename,
            "cb_filename": filename
        }
        return res


class SetLocationInBackground(Resource):
    def put(self):
        args = parser.parse_args()
        filename = args['filename']
        bg_filename = args['bg_filename']
        input_text = args['input_text']
        x = int(args['x_in_bg'])
        y = int(args['y_in_bg'])
        save_dir = "./static/image/"
        img = Image.open(save_dir + filename)
        bg_img = Image.open(save_dir + bg_filename)
        filename = main.combine_bg(img, bg_img, input_text, x, y)

        res = {
            "cb_filename": filename
        }
        return res


class SampleImage(Resource):
    def post(self):
        args = parser.parse_args()
        text = args['latter_list']
        font = int(args['font'])
        latter_num = int(args['latter_num'])
        phoneme_num = int(args['phoneme_num'])
        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        target = latter_list[latter_num][phoneme_num]
        model_num = phoneme_list.index(target.phoneme)
        main.create_sample_image(font, model_num, model_list[font][model_num], sess_list[font][model_num], target.param_list)
        return "success"


api.add_resource(Calligraphy, '/calligraphy')
api.add_resource(ImageOption, '/calligraphy/image')
api.add_resource(PhonemeShapeOption, '/calligraphy/shape')
api.add_resource(PhonemeSizeOption, '/calligraphy/size')
api.add_resource(PhonemeLocationOption, '/calligraphy/location')
api.add_resource(PhonemeRotationOption, '/calligraphy/rotation')
api.add_resource(AddBackGroundImage, '/calligraphy/background')
api.add_resource(SetLocationInBackground, '/calligraphy/background/location')
api.add_resource(SampleImage, '/calligraphy/sample')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
