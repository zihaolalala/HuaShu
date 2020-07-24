# -*- coding: utf-8 -*-
# @Time   : 2020/7/24 9:35
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : data_manager.py
# @Desc   : 

from knowledge_graph.data_management.jianshu_dataloader import JianShuDataLoader

class DataManager:

    data_loaders = {
        'jian_shu': JianShuDataLoader,
    }

    def get_merge_data(self):
        # 从简书获取文章
        data_loader = JianShuDataLoader()
        if not data_loader.load_data():
            # 如果本地没有，从网上爬取
            data_loader.get_data(['机器人故障'])
        return data_loader.url_dict, data_loader.article_dict

    def get_all_data(self):
        # use load data of all data_loaders

        # merge data of all data_loaders

        # return data
        pass
