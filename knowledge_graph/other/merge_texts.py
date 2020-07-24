# -*- coding: utf-8 -*-
# @Time   : 2020/7/2 9:35
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : merge_texts.py
# @Desc   : 

import os
import pickle
from datetime import datetime
from tqdm import tqdm
import glob


if __name__ == '__main__':
    # 获取数据目录
    urls_file = glob.glob('data/*/bin_data.pkl')
    texts_file = glob.glob('data/*/texts_bin_data*.pkl')
    print('# urls_file:\n', '\n'.join(urls_file))
    print('# texts_file:\n', '\n'.join(texts_file))
    # 获取各目录的关键词集合
    text_nums = {}  # 合并前各关键字相关文章的数量
    texts = []  # 合并后所有文章
    texts_url_set = set()  # 合并后所有文章的url
    for file in urls_file:
        with open(file, 'rb') as fin:
            tmp = pickle.load(fin)
            for k, v in tmp.items():
                text_nums[k] = text_nums.get(k, 0) + len(v['urls'])
    print('# {}'.format(text_nums))

    for file in texts_file:
        with open(file, 'rb') as fin:
            tmp = pickle.load(fin)
            for text in tmp:
                if text['url'] in texts_url_set:
                    continue
                else:
                    texts_url_set.add(text['url'])
                    texts.append(text)
    print('合并前文章数：{}，\n合并后文章数：{}'.format(text_nums, len(texts)))
    result = {'text_nums_before_merge': text_nums, 'texts': texts, 'merge_dir': texts_file}

    # 保存到本地
    time_now = str(datetime.now()).replace(' ', '-').replace(':', '')
    with open('merge_texts_{}.pkl'.format(time_now), 'wb') as fout:
        pickle.dump(result, fout)
    with open('merge_texts_{}.txt'.format(time_now), 'wt', encoding='utf-8') as fout:
        fout.write('合并目录：{}\n'.format(result['merge_dir']))
        fout.write('合并前文章数：{}， 合并后文章数：{}\n'.format(result['text_nums_before_merge'], len(result['texts'])))
        for i, text in tqdm(enumerate(result['texts']), 'Saving to local'):
            fout.write('# {} #######################\n'.format(i + 1))
            fout.write('标题：{}\n'.format(text['title']))
            fout.write('url：{}\n'.format(text['url']))
            fout.write('时间：{}， 阅读:{}， 点赞：{}\n'.format(text['time'], text['read_nums'], text['like']))
            fout.write('正文：\n{}\n\n'.format(text['article']))
    print('Finish!')
