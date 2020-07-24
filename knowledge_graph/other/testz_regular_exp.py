# -*- coding: utf-8 -*-
# @Time   : 2020/7/7 13:24
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : testz_regular_exp.py
# @Desc   : 

from tqdm import tqdm
import re


def relation_match(text, word1, word2):
    for k, v in pattern_str_dict.items():
        for _v in v:
            pattern = re.compile(_v.format(word1, word2))
            res = pattern.findall(text)
            if res:
                return True, '{}: {}-{}, {}'.format(k, word1, word2, res)
    return False, None


if __name__ == '__main__':
    # 定义规则 关系类别 具体关系
    pattern_str_dict = dict()
    pattern_str_dict['继承关系'] = []
    pattern_str_dict['整体部分关系'] = []
    pattern_str_dict['其他关系'] = []
    pattern_str_dict['继承关系'].append('({}(属于|是)(一.)?[^,.，。！!]*?{})')
    pattern_str_dict['继承关系'].append('({}这.?{})')
    pattern_str_dict['整体部分关系'].append('{}由[^.,，。！]*{}[^.,，。！]*[组构]成')
    pattern_str_dict['整体部分关系'].append('{}包[括含][^.,，。！]*{}[^.,，。！]*')
    pattern_str_dict['其他关系'].append('({}[^.,，。、!！ _\t\s]+{})')
    test_strs = [
        '广东工业大学-机构-广东工业大学是一种机构',
        '广东工业大学-机构-广东工业大学属于机构',

    ]
    correct_num = 0
    for _str in tqdm(test_strs):
        w1, w2, txt = _str.split('-')
        flag, res = relation_match(txt, w1, w2)
        print('{}-{}'.format(flag, res))
        if flag:
            correct_num += 1
    print('correct num:{}/{}'.format(correct_num, len(test_strs)))
