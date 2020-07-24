# -*- coding: utf-8 -*-
# @Time   : 2020/7/2 12:19
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : simultaneous.py
# @Desc   :

import pickle
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import word2vec
import jieba
import heapq
import numpy as np
from collections import OrderedDict
from tqdm import tqdm
import shutil
import os
import sys

if __name__ == '__main__':
    # 加载文章文件 ################################
    texts_file = '..\\CrawlingData\\merge_texts_2020-07-03-181043.872343.pkl'
    texts_man_file = texts_file[: -3] + 'txt'
    texts = []
    with open(texts_file, 'rb') as fin:
        texts = pickle.load(fin)

    if not (os.path.exists('word_time_dict_all.pkl') and os.path.exists('corpus.txt')):
        # 分词、获得所有词词典 ################################
        corpus = []  # 保存分词后的文章
        word_time_dict = OrderedDict()  # 保存所有词典及其在语料中的出现次数
        word_text_dict = OrderedDict()  # 保存包含某个词的文章的数量
        simultaneous_dict = OrderedDict()
        all_word_times = 0
        all_text_times = len(texts['texts'])
        print('text nums:{}'.format(texts['text_nums_before_merge']))
        print('text dir:{}'.format(texts['merge_dir']))
        for text in tqdm(texts['texts'], 'Spliting texts'):
            # print(text['url'])
            # print(text['title'])
            # print(text['article'])
            # print(text['like'])
            # print(text['read_nums'])
            tmp = text['title'] + '\n' + text['article'] + '\n'
            tmp_split = jieba.lcut(tmp)
            tmp_sen = []
            for i in range(len(tmp_split)):
                tmp_split[i] = tmp_split[i].replace(' ', '')
                if not tmp_split[i] == '':
                    if tmp_split[i] in ',.!?;，。！？；\n':
                        if len(tmp_sen) > 1:
                            for j in range(len(tmp_sen) - 1):
                                for k in range(j + 1, len(tmp_sen)):
                                    if tmp_sen[j] == tmp_sen[k]:
                                        continue
                                    simultaneous_dict[
                                        '{}-{}'.format(tmp_sen[j], tmp_sen[k])] = simultaneous_dict.get(
                                        '{}-{}'.format(tmp_sen[j], tmp_sen[k]), 0) + 1
                            tmp_sen.clear()
                    else:
                        tmp_sen.append(tmp_split[i])
                if not tmp_split[i] == '':
                    word_time_dict[tmp_split[i]] = word_time_dict.get(tmp_split[i], 0) + 1
            corpus.append(' '.join(tmp_split))
            all_word_times += len(tmp_split)
            tmp_set = set(tmp_split)
            for tmp in tmp_set:
                word_text_dict[tmp] = word_text_dict.get(tmp, 0) + 1
        # 将所有词典保存到本地
        word_time_dict = OrderedDict(sorted(word_time_dict.items(), key=lambda item: item[1], reverse=True))
        word_text_dict = OrderedDict(sorted(word_text_dict.items(), key=lambda item: item[1], reverse=True))
        simultaneous_dict = OrderedDict(sorted(simultaneous_dict.items(), key=lambda item: item[1], reverse=True))

        result1 = {'word_time_dict': word_time_dict, 'word_text_dict': word_text_dict,
                   'simultaneous_dict': simultaneous_dict, 'corpus': corpus}
        with open('result1.pkl', 'wb') as fout:
            pickle.dump(result1, fout)
        with open('word_time_dict_all.txt', 'wt', encoding='utf-8') as fout:
            fout.write('# All word nums:{}\n'.format(len(word_time_dict)))
            for k, v in word_time_dict.items():
                fout.write('{}: {}\n'.format(k, v))
        with open('word_text_dict_all.txt', 'wt', encoding='utf-8') as fout:
            fout.write('# All text nums:{}\n'.format(len(corpus)))
            for k, v in word_text_dict.items():
                fout.write('{}: {}\n'.format(k, v))
        with open('simultaneous_dict_all.txt', 'wt', encoding='utf-8') as fout:
            fout.write('# All relation nums:{}\n'.format(len(simultaneous_dict.items())))
            for k, v in simultaneous_dict.items():
                fout.write('{}: {}\n'.format(k, v))
        with open('corpus.txt', 'wt', encoding='utf-8') as fout:
            for i, tmp in enumerate(corpus):
                fout.write('# {} ###############################\n'.format(i + 1))
                fout.write(tmp + '\n')
        print('All word nums:{}'.format(len(word_time_dict)))
    else:
        print('Loading result1.pkl...')
        with open('result1.pkl', 'rb') as fin:
            result1 = pickle.load(fin)
        word_time_dict, word_text_dict, simultaneous_dict, corpus = result1['word_time_dict'], result1['word_text_dict'], result1['simultaneous_dict'], result1['corpus']

    if not os.path.exists('result2.pkl'):
        # 将文本中的词语转换为词频矩阵 ################################
        vectorizer = CountVectorizer()
        # # 计算个词语出现的次数
        print('Counting Vector...')
        X = vectorizer.fit_transform(corpus)
        # 获取词袋中所有文本关键词
        word = vectorizer.get_feature_names()
        print('keyword nums：{}'.format(len(word)))
        # 查看关键词在文章中的出现次数
        # count_array = X.toarray()
        # print(X.toarray())
        # 查看关键词在语料中的出现次数
        keyword_text_dict = OrderedDict()
        keyword_time_dict = OrderedDict()
        for _ in word:
            keyword_text_dict[_] = word_text_dict.get(_, 0)
            keyword_time_dict[_] = word_time_dict.get(_, 0)
        keyword_text_dict = OrderedDict(sorted(keyword_text_dict.items(), key=lambda item: item[1], reverse=True))
        keyword_time_dict = OrderedDict(sorted(keyword_time_dict.items(), key=lambda item: item[1], reverse=True))
        result2 = {'X': X, 'word': word, 'keyword_text_dict': keyword_text_dict, 'keyword_time_dict': keyword_time_dict}
        with open('result2.pkl', 'wb') as fout:
            pickle.dump(result2, fout)
        with open('word_time_dict_key.txt', 'wt', encoding='utf-8') as fout:
            for k, v in keyword_time_dict.items():
                fout.write('{}: {}\n'.format(k, v))
        with open('word_text_dict_key.txt', 'wt', encoding='utf-8') as fout:
            for k, v in keyword_text_dict.items():
                fout.write('{}: {}\n'.format(k, v))
    else:
        with open('result2.pkl', 'rb') as fin:
            result2 = pickle.load(fin)
        X, word = result2['X'], result2['word']

    # 查找词频最高的词的关系
    if not os.path.exists('simultaneous_dict_key.pkl'):
        simultaneous_dict_key = OrderedDict()
        keywords_list = list(keyword_text_dict.keys())
        for i in range(150):
            for j in range(150):
                if i == j:
                    continue
                simultaneous_dict_key['{}-{}'.format(keywords_list[i], keywords_list[j])] = simultaneous_dict.get(
                    '{}-{}'.format(keywords_list[i], keywords_list[j]), 0)
        with open('simultaneous_dict_key.pkl', 'wb') as fout:
            pickle.dump(simultaneous_dict_key, fout)
        with open('simultaneous_dict_key.txt', 'wt', encoding='utf-8') as fout:
            fout.write('# All relation nums:{}\n'.format(len(simultaneous_dict_key.items())))
            for k, v in simultaneous_dict_key.items():
                fout.write('{}: {}\n'.format(k, v))
    else:
        with open('simultaneous_dict_key.pkl', 'rb') as fin:
            simultaneous_dict_key = pickle.load(fin)

    # TF-IDF
    transformer = TfidfTransformer()
    # 将词频矩阵X统计成TF-IDF值
    print('Calculating TF-IDF...')
    tfidf = transformer.fit_transform(X)
    # 查看数据结构 tfidf[i][j]表示i个文本中的关键词的tf-idf权重
    tfidf_array = tfidf.toarray()
    # print(tfidf_array.shape)
    # print(tfidf_array)

    # keywords_array = []
    # keywords_set = set()
    # for line in tqdm(tfidf_array, ''):
    #     line = np.array(line)
    #     indexs = np.argsort(line)[-20:]
    #     keyword = [word[i] for i in indexs]
    #     # line_dict = dict(zip(line, list(range(len(line)))))
    #     # key_index = heapq.nlargest(5, line_dict)
    #     # key_word = list(map(lambda x: tfidf_array[x], key_index))
    #     keywords_array.append(keyword)
    #     keywords_set = keywords_set.union(keyword)
    # print(len(keywords_set))
    # print(keywords_array[:10])
