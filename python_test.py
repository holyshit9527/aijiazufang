# encoding: utf-8
"""
@version: 1.0
@author: 
@file: python_test
@time: 2020/2/3 16:50
"""


class MusicPlayer:
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        if MusicPlayer.init_flag:
            return
        print("初始化播放器！")
        MusicPlayer.init_flag = True


p1 = MusicPlayer()
p2 = MusicPlayer()
print(p1)
print(p1)
