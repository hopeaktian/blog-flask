#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/1 12:09
author:    peak
description:
"""
class Config(object):
    SECRET_KEY = ''

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Yourpassword@yourdomain:3306/blog"
