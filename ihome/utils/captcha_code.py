# encoding: utf-8
"""
@version: 1.0
@author: 
@file: captcha_test
@time: 2020/2/2 10:43
"""
from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
from io import StringIO


class Captcha:
    def __init__(self):
        # 验证码中的字符, 就不用汉字了
        self.number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                         'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def random_captcha_text(self, captcha_size=4):
        # 验证码一般都无视大小写；验证码长度4个字符
        char_set = self.number + self.alphabet + self.ALPHABET
        captcha_text = []
        for i in range(captcha_size):
            c = random.choice(char_set)
            captcha_text.append(c)
        return captcha_text

    def gen_captcha_text_and_image(self, fmt='JPEG'):
        # 生成字符对应的验证码
        image = ImageCaptcha()

        captcha_text = self.random_captcha_text()
        captcha_text = ''.join(captcha_text)

        captcha_raw = image.generate(captcha_text)
        # image.write(captcha_text, captcha_text + '.jpg')  # 写到文件

        # captcha_image = Image.open(captcha)
        # print(type(captcha_image))
        # print(captcha_image)
        # captcha_image = np.array(captcha_image)
        return captcha_text, captcha_raw.getvalue()


captcha = Captcha()

if __name__ == '__main__':
    # 测试
    text, image = captcha.gen_captcha_text_and_image()
    print(text)
    print(image)

    # f = plt.figure()
    # ax = f.add_subplot(111)
    # ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)
    # plt.imshow(image)
    #
    # plt.show()

