# -*- coding: utf-8 -*-
# @Time   : 2020/7/24 9:35
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : data_manager.py
# @Desc   :
from collections import OrderedDict

from tqdm import tqdm
from knowledge_graph.data_management.dataloader_jianshu import JianShuDataLoader
from knowledge_graph.data_management.dataloader_csdn import CsdnDataLoader
from LAC import LAC
from knowledge_graph.utils.log_utils import log_print
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class DataManager:

    lac = LAC()

    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.data_loaders = {
            # 'jian_shu': JianShuDataLoader(work_dir),
            'csdn': CsdnDataLoader(work_dir),
        }

    def get_url_article(self, keywords):
        self.url_dict, self.article_dict = {}, {}
        for keyword in keywords:
            self.url_dict[keyword] = set()

        for loader_name, data_loader in self.data_loaders.items():
            flag, missing_keys = data_loader.load_url_article(keywords)
            if not flag:
                data_loader.get_url_articl(missing_keys)
            # merge data
            for keyword in keywords:
                for url in data_loader.url_dict[keyword]:
                    article = data_loader.article_dict.get(url, None)
                    if article is not None:
                        if data_loader.FILTER.filter_when_loading(keyword, article[0], article[5]):
                            self.url_dict[keyword].add(url)
                            if url not in self.article_dict:
                                self.article_dict[url] = article
        return self.url_dict, self.article_dict

    @staticmethod
    def cut_lac(sentence):
        return DataManager.lac.run(sentence)

    def get_word_frequency(self):
        # word_dict: word-(sk-keyword sk-tfidf time idf paper_keyword)
        # simultaneous_dict: word1_2-(sentimes subsentimes)
        assert hasattr(self, 'url_dict') and hasattr(self, 'article_dict'), 'Please get(and merge) url and article before getting word frequency!'
        # 分词、获得所有词词典 ################################
        self.word_dict = OrderedDict()  # 保存所有词典及其在语料中的出现次数
        self.simultaneous_dict = OrderedDict()  # 保存包含某个词的文章的数量
        log_print('Article nums:{}'.format(len(self.article_dict)))
        self.segmentation, self.segmentation_pos = [], []
        all_word_times = 0
        for url, article in tqdm(self.article_dict.items(), 'Spliting texts'):
            # str:title, int:read_nums, int:like_nums, str:time, list:keywords, str:abstract,
            # str:article.text, list:segmentation
            tmp = article[0] + '\n' + article[6]
            cut_result = self.cut_lac(tmp)

            tmp_ws = []
            tmp_pos = []
            for i in range(len(cut_result[0])):
                # cut_result[0][i] = cut_result[0][i].replace(' ', '')
                if cut_result[0][i] != '':
                    if cut_result[0][i] in ',.!?;，。！？；\n':
                        # 只输出动词和名词
                        # for j in range(1, len(tmp_pos) - 1):
                        #     if tmp_pos[j] == 'v':
                        #         for k in range(j - 1, 0, -1):
                        #             if tmp_pos[k] == 'v':
                        #                 start = k
                        #                 break
                        #         for _ in range(k + 1, j):
                        #             print(tmp_ws[_], end='-')
                        #         print('[[{}]]'.format(tmp_ws[j]), end='-')
                        #         for k in range(j + 1, len(tmp_pos)):
                        #             if tmp_pos[k] != 'v':
                        #                 print(tmp_ws[k], end='-')
                        #             else:
                        #                 break
                        #         print()

                        # 输出所有词，动词用中括号标记
                        for j in range(len(tmp_pos)):
                            if tmp_pos[j] in ['v', 'vd']:
                                print('-[[{}]]-'.format(tmp_ws[j]), end='')
                            else:
                                print('-{}-'.format(tmp_ws[j]), end='')
                        print()
                        # if len(tmp_ns) > 1:
                        #     for j in range(len(tmp_ns) - 1):
                        #         for k in range(j + 1, len(tmp_ns)):
                        #             if tmp_ns[j] == tmp_ns[k]:
                        #                 continue
                        #             self.simultaneous_dict[
                        #                 '{}-{}'.format(tmp_ns[j], tmp_ns[k])] = self.simultaneous_dict.get(
                        #                 '{}-{}'.format(tmp_ns[j], tmp_ns[k]), 0) + 1
                        tmp_ws.clear()
                        tmp_pos.clear()
                    else:
                        # if cut_result[1][i] in ['n', 'f', 's', 'nw', 'nz', 'v']:
                        tmp_ws.append(cut_result[0][i])
                        tmp_pos.append(cut_result[1][i])

                if cut_result[0][i] not in self.word_dict:
                    self.word_dict[cut_result[0][i]] = [0] * 5
                self.word_dict[cut_result[0][i]][2] = self.word_dict.get(cut_result[0][i])[2] + 1
            self.segmentation.append(cut_result[0])
            self.segmentation_pos.append(cut_result[1])
            all_word_times += len(cut_result[0])

            cut_result_set = set(cut_result[0])
            for word in cut_result_set:
                self.word_dict[word][3] = self.word_dict.get(word)[3] + 1

            keywords = article[4]
            for keyword in keywords:
                if keyword not in self.word_dict:
                    self.word_dict[keyword] = [0] * 5
                self.word_dict[keyword][4] = 1

        # 将文本中的词语转换为词频矩阵 ################################
        vectorizer = CountVectorizer()
        # # 计算个词语出现的次数
        log_print('Counting words by sklearn...')
        corpus = [' '.join(text) for text in self.segmentation]
        X = vectorizer.fit_transform(corpus)
        # 获取词袋中所有文本关键词
        words = vectorizer.get_feature_names()
        log_print('keyword nums：{}'.format(len(words)))
        # 查看关键词在文章中的出现次数
        # count_array = X.toarray()
        # print(X.toarray())
        # 查看关键词在语料中的出现次数
        for word in words:
            if word not in self.word_dict:
                self.word_dict[word] = [0] * 5
            self.word_dict[word][0] = 1

        # 不再统计TF-IDF
        # transformer = TfidfTransformer()
        # # 将词频矩阵X统计成TF-IDF值
        # log_print('Calculating TF-IDF by sklearn...')
        # tfidf = transformer.fit_transform(X)
        # # 查看数据结构 tfidf[i][j]表示i个文本中的关键词的tf-idf权重
        # tfidf_array = tfidf.toarray()

        # 将所有词典保存到本地
        # self.save_word_info()
        return self.word_dict, self.simultaneous_dict

    def save_word_info(self):
        # result = {'word_dict': self.word_dict, 'simultaneous_dict': self.simultaneous_dict,
        #            'corpus': self.corpus}
        # with open('result1.pkl', 'wb') as fout:
        #     pickle.dump(result1, fout)
        # with open('word_time_dict_all.txt', 'wt', encoding='utf-8') as fout:
        #     fout.write('# All word nums:{}\n'.format(len(word_time_dict)))
        #     for k, v in word_time_dict.items():
        #         fout.write('{}: {}\n'.format(k, v))
        # with open('word_text_dict_all.txt', 'wt', encoding='utf-8') as fout:
        #     fout.write('# All text nums:{}\n'.format(len(corpus)))
        #     for k, v in word_text_dict.items():
        #         fout.write('{}: {}\n'.format(k, v))
        # with open('corpus.txt', 'wt', encoding='utf-8') as fout:
        #     for i, tmp in enumerate(corpus):
        #         fout.write('# {} ###############################\n'.format(i + 1))
        #         fout.write(tmp + '\n')
        # log_print('All word nums:{}'.format(len(word_time_dict)))
        pass
