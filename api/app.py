from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import numpy as np
import load_model
import cv2
import os
from urllib import parse
import main
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
parser.add_argument('definition')
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
        param_list = [0] * 4
        definition = 50
        color = [0, 0, 0]
        is_invisiable = True
        text, shape_list = main.convert_text(input_text)
        latter_list, json_latter_list = main.create_latter_list(font, model_list, sess_list, text, shape_list, param_list)
        filename, _, image_width, image_height = main.img_attach(latter_list, definition, color, is_invisiable, input_text, None)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "latter_list": json_latter_list,
            "filename": filename,
            "definition": definition,
            "color": color,
            "image_width": image_width,
            "image_height": image_height
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
        definition = int(args['definition'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        color = json.loads(args['color'])
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
        target_img = main.create_one_image(target, model_list[font][model_num],  sess_list[font][model_num])
        target_img = cv2.resize(target_img, (int(target.width), int(target.height)), interpolation=cv2.INTER_LINEAR)
        target_img = main.update_rotation(target_img, target.rotation)
        target.img = target_img
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, definition, color, is_invisiable, input_text, bg_data, image_width, image_height)

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
        color = json.loads(args['color'])
        definition = int(args['definition'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
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
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, definition, color, is_invisiable, input_text, bg_data, image_width, image_height)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "filename": filename,
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
        color = json.loads(args['color'])
        definition = int(args['definition'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
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
        target.img = target.img.astype(np.uint8)
        target_img = cv2.resize(target.img, (int(target.width), int(target.height)), interpolation=cv2.INTER_LINEAR)
        latter_list[latter_num][phoneme_num].img = target_img
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, definition, color, is_invisiable, input_text, bg_data, image_width, image_height)

        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
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
        color = json.loads(args['color'])
        definition = int(args['definition'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
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
        target_img = main.create_one_image(target, model_list[font][model_num], sess_list[font][model_num])
        target_img = cv2.resize(target_img, (int(target.width), int(target.height)), interpolation=cv2.INTER_LINEAR)
        target_img = main.update_rotation(target_img, target.rotation)
        target.img = target_img
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, definition, color, is_invisiable, input_text, bg_data, image_width, image_height)

        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
            "latter_list": text
        }
        return res


# 전체 이미지 옵션 수정
class ImageOption(Resource):
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        definition = int(args['definition'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        color = json.loads(args['color'])
        is_invisiable = int(args['is_invisiable'])
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
        filename, cb_filename, image_width, image_height = main.img_attach(latter_list, definition, color, is_invisiable, input_text, bg_data, image_width, image_height)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "latter_list": text,
            "filename": filename,
            "definition": definition,
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
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "bg_filename": bg_filename,
            "cb_filename": filename
        }
        return res


api.add_resource(Calligraphy, '/calligraphy')
api.add_resource(ImageOption, '/calligraphy/image')
api.add_resource(PhonemeShapeOption, '/calligraphy/shape')
api.add_resource(PhonemeSizeOption, '/calligraphy/size')
api.add_resource(PhonemeLocationOption, '/calligraphy/location')
api.add_resource(PhonemeRotationOption, '/calligraphy/rotation')
api.add_resource(AddBackGroundImage, '/calligraphy/background')

if __name__ == '__main__':
    app.run(debug=False)
