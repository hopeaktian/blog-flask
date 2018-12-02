#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/2 14:14
author:    peak
description:
"""
import markdown



css = u'''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!-- 此处省略掉markdown的css样式，因为太长了 -->
</style>
'''

def switch_html(file):
    with open(file, 'rb') as f:
        try:
            text = f.read()
            text = text.decode('utf-8')
            html = markdown.markdown(text)
            newhtml = html
        except:
            return None
        else:
            return newhtml

