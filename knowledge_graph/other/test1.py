# -*- coding: utf-8 -*-
# @Time   : 2020/7/13 1:27
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : test1.py
# @Desc   : 

import sys


def check_contain_chinese(check_str):
    for ch in check_str:
        print(check_str.encode('utf-8'))
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


if __name__ == "__main__":
    print(check_contain_chinese('i love yiu '))
    print(check_contain_chinese('i love you'))
    print(check_contain_chinese('xx中国'))
