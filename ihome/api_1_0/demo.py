# encoding: utf-8
"""
@version: 1.0
@author: 
@file: demo
@time: 2020/1/31 13:16
"""
from . import api
import logging
from ihome import db, models
from flask import current_app


@api.route('/index')
def index():
    # 额外添加日志的方式
    current_app.logger.error('this is error')
    current_app.logger.warn('this is warn')

    return "hello index"
