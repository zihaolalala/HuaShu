# -*- coding: utf-8 -*-
# @Time   : 2020/7/4 19:59
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : log_utils.py
# @Desc   : 

import logging
import traceback
import os

# 设置日志文件
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
log_file = open(os.path.join(log_dir, 'KnowledgeGraph.log'), 'wt', encoding='utf-8')
handler = logging.StreamHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_print(content):
    s = traceback.extract_stack()
    call_file = s[-2][0][s[-2][0].rfind('HuaShu'):]
    print(content)
    logger.info('{}: {}'.format(call_file, content))


def log_close():
    log_file.close()
