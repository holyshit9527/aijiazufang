# encoding: utf-8
"""
@version: 1.0
@author: 
@file: __init__.py
@time: 2020/1/31 10:59
"""
from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect

import redis
import logging
from logging.handlers import RotatingFileHandler

from ihome.utils.commons import ReConverter


# 数据库
db = SQLAlchemy()
# redis
redis_store = None


# 配置日志

# 创建日志记录器，指明日志保存的路径，每个日志文件的最大大小，保存的日志文件个数上限
file_log_handler = RotatingFileHandler('logs/log.log', maxBytes=1024*1024*50, backupCount=5)
# 创建日志记录的格式  时间，日志等级，输入日志信息的文件名，函数名称，行数，日志信息
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象添加日志记录器 --flask app
logging.getLogger().addHandler((file_log_handler))
# 设置日志记录等级
logging.basicConfig(level=logging.DEBUG)

"""
%(asctime)s - %(filename)s:%(lineno)s - %(levelno)s %(levelname)s %(pathname)s %(module)s %(funcName)s %(created)f %(thread)d %(threadName)s %(process)d %(name)s - %(message)s
%(name)s	生成日志的Logger名称。
%(levelno)s	数字形式的日志级别，包括DEBUG, INFO, WARNING, ERROR和CRITICAL。
%(levelname)s	文本形式的日志级别，包括’DEBUG’、 ‘INFO’、 ‘WARNING’、 ‘ERROR’ 和’CRITICAL’。
%(pathname)s	输出该日志的语句所在源文件的完整路径（如果可用）。
%(filename)s	文件名。
%(module)s	输出该日志的语句所在的模块名。
%(funcName)s	调用日志输出函数的函数名。
%(lineno)d	调用日志输出函数的语句所在的代码行（如果可用）。
%(created)f	日志被创建的时间，UNIX标准时间格式，表示从1970-1-1 00:00:00 UTC计算起的秒数。
%(relativeCreated)d	日志被创建时间与日志模块被加载时间的时间差，单位为毫秒。
%(asctime)s	日志创建时间。默认格式是 “2003-07-08 16:49:45,896”，逗号后为毫秒数。
%(msecs)d	毫秒级别的日志创建时间。
%(thread)d	线程ID（如果可用）。
%(threadName)s	线程名称（如果可用）。
%(process)d	进程ID（如果可用）。
%(message)s	日志信息。
"""


# 工程模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str, 配置模式的模式名称， （‘product’， ‘develop’）
    :return:
    """
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)
    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST,
                                    port=config_class.REDIS_PORT,
                                    decode_responses=config_class.REDIS_DECODE_RESPONSES)
    # 利用flask-session，将session数据保存到redis中
    Session(app)
    # 为flask提供CSRF防护
    CSRFProtect(app)
    # flask添加自定义的转化器
    app.url_map.converters['re'] = ReConverter
    # 注册蓝图
    from ihome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')
    # 注册提供静态文件的蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)



    return app
