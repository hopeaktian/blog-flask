#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/1 12:07
author:    peak
description:
"""
from flask import Flask, redirect, url_for, render_template, session, g, jsonify, request
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(host='192.168.3.5', port=80)