# encoding: utf-8
"""
@version: 1.0
@author: 
@file: common
@time: 2020/1/31 19:02
"""
from werkzeug.routing import BaseConverter


# 定义正则转化器
class ReConverter(BaseConverter):
    """"""
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法1
        super(ReConverter, self).__init__(url_map)
        self.regex = regex
