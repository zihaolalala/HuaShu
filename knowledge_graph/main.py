# -*- coding: utf-8 -*-
# @Time   : 2020/7/24 23:53
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : main.py
# @Desc   : 

import os
import sys
cmd_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not cmd_path in sys.path:
    sys.path.append(cmd_path)

from knowledge_graph.data_management.data_manager import DataManager
from knowledge_graph.concept_management.concept_manager import ConceptManager
from knowledge_graph.relation_management.relation_manager import RelationManager

from knowledge_graph.utils.log_utils import log_print, log_close
from knowledge_graph.utils.path_utils import create_work_dir

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

if __name__ == '__main__':
    # 创建工作区
    work_dir = create_work_dir('data/knowledge_graph/ex1/')

    # 1 获取语料
    data_manager = DataManager(work_dir)
    # 1.1 获取url、文章
    url_dict, article_dict = data_manager.get_url_article(['机器人故障'])
    # 1.2 统计词频，获取词典、两词语同时出现的次数统计
    word_dict, simultaneous_dict = data_manager.get_word_frequency()

    # # 2 获取概念
    # concept_manager = ConceptManager(work_dir)
    # concept_dict = concept_manager.get_concept(article_dict, word_dict, simultaneous_dict)
    #
    # # 3 关系抽取
    # relation_manager = RelationManager(work_dir)
    # relation_result = relation_manager.get_relation(concept_dict, article_dict)
    #
    log_print('Finish!')
    log_close()
    pass
