# -*- coding: utf-8 -*-
# @Time   : 2020/7/4 19:59
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : log_utils.py
# @Desc   : 

import logging
import traceback

# 设置日志文件
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_file = open('KnowledgeGraph.log', 'wt', encoding='utf-8')
handler = logging.StreamHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_print(content):
    s = traceback.extract_stack()
    call_file = s[-2][0][s[-2][0].rfind('HuaShu'):]
    print(content)
    logger.info('{}: {}\n'.format(call_file, content))
