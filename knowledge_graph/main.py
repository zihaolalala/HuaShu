# -*- coding: utf-8 -*-
# @Time   : 2020/7/24 23:53
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : main.py
# @Desc   : 

from knowledge_graph.data_management import data_manager
from knowledge_graph.concept_management import concept_manager
from knowledge_graph.relation_management import relation_manager

from knowledge_graph.utils.log_utils import log_print

if __name__ == '__main__':
    # 获取语料
    data_manager_ = data_manager.DataManager()
    # url和文章
    url_dict, article_dict = data_manager_.get_merge_data()
    print(url_dict, article_dict)

    # 获取概念
    concept_manager_ = concept_manager.ConceptManager()
    # 统计候选概念
    concept_dict = concept_manager_.get_concept(url_dict, article_dict)

    # 关系抽取
    relation_manager_ = relation_manager.RelationManager()
    relation_result = relation_manager_.get_relation(concept_dict, article_dict)
    pass



