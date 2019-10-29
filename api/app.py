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
parser.add_argument('color')
parser.add_argument('background_image', type=werkzeug.datastructures.FileStorage, location='files')
parser.add_argument('filename')
phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
    , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']


class Calligraphy(Resource):

    def get(self):
        return 'hi'

    def post(self):
        args = parser.parse_args()
        font = int(args['font'])
        input_text = args['input_text']
        param_list = [-1] * 4
        definition = 50
        color = [0, 0, 0]
        text, shape_list = main.convert_text(input_text)
        latter_list, json_latter_list = main.create_latter_list(font, model_list, sess_list, text, shape_list, param_list)
        filename = main.img_attach(latter_list, definition, color, input_text)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "latter_list": json_latter_list,
            "filename": filename,
            "definition": definition,
            "color": color
        }
        return res

    def put(self):
        args = parser.parse_args()
        font = int(args['font'])
        latter_num = int(args['latter_num'])
        phoneme_num = int(args['phoneme_num'])
        text = args['latter_list']
        input_text = args['input_text']
        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        model_num = phoneme_list.index(latter_list[latter_num][phoneme_num].phoneme)
        target_img = main.create_one_image(latter_list[latter_num][phoneme_num], model_list[font][model_num], sess_list[font][model_num])
        if target_img.shape[1] != latter_list[latter_num][phoneme_num].width or target_img.shape[0] != latter_list[latter_num][phoneme_num].height:
            target_img = cv2.resize(target_img, (int(latter_list[latter_num][phoneme_num].width), int(latter_list[latter_num][phoneme_num].height)), interpolation=cv2.INTER_LINEAR)
        latter_list[latter_num][phoneme_num].img = target_img
        filename = main.img_attach(latter_list, 40, 0, input_text)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
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
        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        model_num = phoneme_list.index(latter_list[latter_num][phoneme_num].phoneme)
        target_img = main.create_one_image(latter_list[latter_num][phoneme_num], model_list[font][model_num],
                                           sess_list[font][model_num])
        latter_list[latter_num][phoneme_num].img = target_img
        filename = main.img_attach(latter_list, 40, 0, input_text)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
            "latter_list": text
        }
        return res


# 이미지 위치 조정
class PhonemeLocationOption(Resource):
    def put(self):
        args = parser.parse_args()
        text = args['latter_list']
        input_text = args['input_text']
        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        filename = main.img_attach(latter_list, 40, 0, input_text)
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
        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        target_img = cv2.resize(latter_list[latter_num][phoneme_num].img, (int(latter_list[latter_num][phoneme_num].width),
                                             int(latter_list[latter_num][phoneme_num].height)),
                                interpolation=cv2.INTER_LINEAR)
        filename = main.img_attach(latter_list, 40, 0, input_text)

        com = 's3cmd put ./static/image/{}.png s3://seolo/static/image/'.format(filename)
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
        latter_list = args['latter_list']
        definition = int(args['definition'])
        image_width = int(args['image_width'])
        image_height = int(args['image_height'])
        color = args['color']
        input_text = args['input_text']
        filename = main.img_attach(latter_list, definition, color, input_text, image_width, image_height)
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "latter_list": latter_list,
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
        background_image = args['background_image']
        img_path = './static/image/{}'.format(filename)
        img = Image.open(img_path)
        background_image.paste(img, (0, 0), img)
        filename = "bg_"+filename
        background_image.save("./static/image/{}".format(filename))
        com = 's3cmd put ./static/image/{} s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "bg_filename": filename
        }
        return res


api.add_resource(Calligraphy, '/calligraphy')
api.add_resource(ImageOption, '/calligraphy/image')
api.add_resource(PhonemeShapeOption, '/calligraphy/shape')
api.add_resource(PhonemeSizeOption, '/calligraphy/size')
api.add_resource(PhonemeLocationOption, '/calligraphy/location')
api.add_resource(AddBackGroundImage, '/calligraphy/background')

if __name__ == '__main__':
    app.run(debug=False)
