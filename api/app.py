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

phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ'
    , 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']



class Calligraphy(Resource):
    def get(self):
        return 'hi'
    def post(self):
        args = parser.parse_args()
        font = args['font']
        input_text = args['input_text']
        param_list = [-1] * 4
        text, shape_list = main.convert_text(input_text)
        latter_list, json_latter_list = main.create_latter_list(model_list, sess_list, text, shape_list, param_list)
        filename = main.img_attach(latter_list, 70, 0, input_text)
        com = 's3cmd put ./static/image/{}.png s3://seolo/static/image/'.format(filename)
        os.system(com)
        res = {
            "filename": filename,
            "latter_list": json_latter_list
        }
        return res
    def put(self):
        args = parser.parse_args()
        latter_num = int(args['latter_num'])
        phoneme_num = int(args['phoneme_num'])
        text = args['latter_list']
        input_text = args['input_text']
        text = text.replace("'", "\"")
        text = json.loads(text)
        latter_list = main.json_to_obj(text)
        model_num = phoneme_list.index(latter_list[latter_num][phoneme_num].phoneme)
        target_img = main.create_one_image(latter_list[latter_num][phoneme_num], model_list[model_num], sess_list[model_num])
        if target_img.shape[1] != latter_list[latter_num][phoneme_num].width or target_img.shape[0] != latter_list[latter_num][phoneme_num].height:
            target_img = cv2.resize(target_img, (int(latter_list[latter_num][phoneme_num].width), int(latter_list[latter_num][phoneme_num].height)), interpolation=cv2.INTER_LINEAR)
        latter_list[latter_num][phoneme_num].img = target_img
        filename = main.img_attach(latter_list, 70, 0, input_text)
        com = 's3cmd put ./static/image/{}.png s3://seolo/static/image/'.format(filename)
        os.system(com)
        text[latter_num][phoneme_num]['img'] = target_img.tolist()
        res = {
            "filename": filename,
            "latter_list": text
        }
        return res


api.add_resource(Calligraphy, '/calligraphy')

if __name__ == '__main__':
    app.run(debug=False)
