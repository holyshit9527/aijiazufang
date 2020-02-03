# encoding: utf-8
"""
@version: 1.0
@author: 
@file: web_html
@time: 2020/1/31 17:46
"""
from flask import Blueprint, current_app, make_response
from flask_wtf import csrf

# 提供静态文件1的蓝图
html = Blueprint('web_html', __name__)


@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    """提供html文件"""
    # 如果html_file_name为“”，表示访问的路径1是/，请求的是主页
    if not html_file_name:
        html_file_name = "index.html"
    # 文件在html目录下,如果文件名称不是网站的logo就添加位置信息
    if html_file_name != "favicon.ico":
        html_file_name = "html/" + html_file_name
    # csrf值
    csrf_token = csrf.generate_csrf()
    # flask提供的返回静态文件的方法
    resp = make_response(current_app.send_static_file(html_file_name))
    # 设置cookie
    resp.set_cookie('csrf_token', csrf_token)

    return resp
