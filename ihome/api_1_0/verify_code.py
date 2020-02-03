# encoding: utf-8
"""
@version: 1.0
@author: 
@file: verify_code
@time: 2020/2/1 12:01
"""
from flask import current_app, jsonify, make_response, request
from . import api
from ihome import redis_store, constants
from ihome.utils.captcha_code import captcha
from ihome.utils.response_code import RET
from ihome.models import User
import random

# GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>
@api.route("/image_codes/<image_codes_id>")
def get_image_code(image_codes_id):
    # 生成名字、真是文本、图片数据
    text, image_data = captcha.gen_captcha_text_and_image()
    try:
        redis_store.setex("image_code_%s" % image_codes_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录异常信息
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmg="save image code id error!")
    resp = make_response(image_data)
    # 修改返回的文件类型
    resp.headers['Content-Type'] = 'image/jpg'

    return resp


# GET /api/v0.1/sms_codes/<mobile>?image_code=xxx&image_code_id=xxxx
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    # 检验参数
    if not all([image_code, image_code_id]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmg="参数不完整")

    # 校验图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmg="数据库异常")

    # 图片验证码是否过期
    if real_image_code is None:
        return jsonify(errno=RET.NODATA, errmg="图片验证码失效")
    # 删除图片验证码，防止使用同一个验证码对此验证
    try:
        redis_store.delect("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 判断验证码是否正确
    if real_image_code.lower() != image_code.lower():
        # 用户填写错误
        print(real_image_code.lower(), image_code.lower())
        return jsonify(errno=RET.DATAERR, errmg="图片验证码错误")
    # 判断手机号码是否在60s内发送过短信
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            # 有过发送记录，返回错误
            return jsonify(errno=RET.REQERR, errmg="请求过于频繁，请于60S后发送")
    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 手机号已经存在
            return jsonify(errno=RET.DATAEXIST, errmg="手机号已经存在")

    # 手机号码不存在，生成短信验证码
    sms_code = "%6d" % random.randint(0, 999999)
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送记录
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmg="保存短信验证码异常")
    # 发送短信
    print(sms_code, mobile)
    return jsonify(errno=RET.OK, errmg="发送成功")