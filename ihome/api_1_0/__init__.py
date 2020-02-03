# encoding: utf-8
"""
@version: 1.0
@author: 
@file: __init__.py
@time: 2020/1/31 11:17
"""
from flask import Blueprint

# 创建蓝图对象
api = Blueprint('api_1_0', __name__)
# 导入识图蓝图
from . import demo, verify_code
