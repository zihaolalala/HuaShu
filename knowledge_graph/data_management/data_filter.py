# -*- coding: utf-8 -*-
# @Time   : 2020/7/24 9:47
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : data_filter.py
# @Desc   : 


class DataFilter:

    @staticmethod
    def filter_when_getting(keyword, title, abstract):
        return True

    @staticmethod
    def filter_when_loading(keyword, title, abstract):
        if ('机器人' in title) and ('故障' in title):
            return True
        return False

    def manual_filter(self, data):
        pass
