import os
import subprocess
from flask import Flask,request,jsonify
import json
import torch
from model.models import *

# 后端服务启动
app = Flask(__name__)
ASRmodel = ASR('/data/sdb2/lzy/LLM/whisper-large-v3')
config=None
docEncoder = DocEncoder('/data/sdb2/wyh/models/bert-base-chinese','cuda',128)
@app.route("/doc_encode",methods=['post','get'])
def doc_encode():
    torch.cuda.empty_cache()
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        docs = data['docs']
        doc_encoded=docEncoder.encode(docs)
        formResult = {"resultinfo":doc_encoded}
        print('Normal Reponse:',"文档编码接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

vLmodel = VLmodel('/data/sdb2/lzy/LLM/Qwen2-VL-7B-Instruct')
@app.route("/pic2doc",methods=['post','get'])
def pic2doc():
    torch.cuda.empty_cache()
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        prompt = data['prompt']
        pic_paths = data['pic_paths']
        docs = [vLmodel.askmodel(prompt,one) for one in pic_paths]
        formResult = {"resultinfo":docs}
        print('Normal Reponse:',"图片生文档接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

picEncoder = PicEncoder('/data/sdb2/wyh/models/vit-base-patch16-224','cuda')
@app.route("/pic_encode",methods=['post','get'])
def pic_encode():
    torch.cuda.empty_cache()
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        pic_paths = data['pic_paths']
        pic_encoded = picEncoder.encode(pic_paths)
        formResult = {"resultinfo":pic_encoded}
        print('Normal Reponse:',"图片编码接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

CLIPmode = Clip_Sim()
@app.route("/CLIPmodel",methods=['post','get'])
def CLIPmodel():
    torch.cuda.empty_cache()
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        pic_paths = data['pic_paths']
        text = data['text']
        sim = [CLIP.calculate_similarity(item,text[i]) for i,item in enumerate(pic_paths)]
        formResult = {"resultinfo":sim}
        print('Normal Reponse:',"图文向量相似度接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

audioEncoder = AudioEncoder(('/data/sdb2/wyh/models/clap-htsat-unfused','cuda'))
@app.route("/audio_encode",methods=['post','get'])
def audio_encode():
    torch.cuda.empty_cache()
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        audios = data['audios']
        audio_encoded = audioEncoder.encode(audios)
        formResult = {"resultinfo":audio_encoded}
        print('Normal Reponse:',"音频编码接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

@app.route("/audio2text",methods=['post','get'])
def audio_encode():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        audios = data['audios']
        audio_encoded = ASRmodel.Audio2text(audios)
        formResult = {"resultinfo":audio_encoded}
        print('Normal Reponse:',"音频转文本接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

Qwen2 = LoadLLM('/data/sdb2/lzy/LLM/Qwen2-7B-Instruct')
@app.route("/discrimination",methods=['post','get'])
def discrimination():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        text = data['text']
        response = Qwen2.discrimination(text)
        formResult = {"resultinfo":response}
        print('Normal Reponse:',"文本偏见歧视接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

@app.route("/valid",methods=['post','get'])
def LogicalLegality():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        text = data['text']
        response = Qwen2.valid(text)
        formResult = {"resultinfo":response}
        print('Normal Reponse:',"文本现实逻辑接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

@app.route("/guideline",methods=['post','get'])
def LogicalLegality():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        text_pair = data['text_pair']
        rule = data['rule']
        response = Qwen2.labelOK(rule,text_pair)
        formResult = {"resultinfo":response}
        print('Normal Reponse:',"文本标注规则接口调用成功")
        return jsonify(formResult)
    return 'connection ok!'

if __name__ == '__main__':
    app.config['JSON_AS_ASCII']=False
    app.run(host='0.0.0.0',port=48812)
    print("GoodBye")
