# -*- coding: utf-8 -*-
# @Time   : 2020/7/24 9:35
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : data_manager.py
# @Desc   : 

from knowledge_graph.data_management.dataloader_jianshu import JianShuDataLoader


class RelationManager:

    def get_relation(self, concept_dict, article_dict):
        # 统计概念间的关系强度

        # 制定常用关系的正则表达式

        # 加载词性标注模型

        # 对于有强相关关系的两个词语同时出现的句子
        # 1. 从文章中匹配常用关系，得到关系结果
        # 2. 如果第1步匹配失败，用词性标注模型预测句子中每个词的词性，将动词作为这两个词的关系，，得到关系结果

        # 保存并返回所有的关系

        pass
