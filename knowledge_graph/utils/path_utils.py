# -*- coding: utf-8 -*-
# @Time   : 2020/7/29 12:39
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : path_utils.py
# @Desc   : 

import os


def create_work_dir(work_dir):
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    return work_dir
