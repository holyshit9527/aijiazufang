# encoding: utf-8
"""
@version: 1.0
@author: 
@file: config
@time: 2020/1/31 10:09
"""
import redis


class Config(object):
    """配置信息"""
    SECRET_KEY = "xjkfjl%$#2xjk"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:910812@127.0.0.1:3306/aijiazufang"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DECODE_RESPONSES = True

    # flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookes id中的session_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # session数据源的有效时间，单位是秒


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    pass


class ProductionConfig(Config):
    """生产环境配置"""
    pass


# 类名映射
config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}