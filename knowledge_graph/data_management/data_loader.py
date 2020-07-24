# -*- coding: utf-8 -*-
# @Time   : 2020/7/21 21:08
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : data_loader.py
# @Desc   : 

import os
import logging
import pickle
from collections import OrderedDict
from knowledge_graph.data_management import data_loader, data_filter
import selenium.common
import selenium.webdriver
import urllib.parse
import time
import pickle
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os
import platform
from datetime import datetime
import random
from knowledge_graph.utils.selenium_utils import time_out_tips
from knowledge_graph.utils.log_utils import log_print
import os

class DataLoader:

    # 设置chrome浏览器无界面模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    if platform.system() == 'Windows':
        BROWSER = selenium.webdriver.Chrome(executable_path=os.path.join(os.path.abspath('./data_management/'), 'chromedriver.exe'),
                                            chrome_options=chrome_options)
    elif platform.system() == 'Linux':
        BROWSER = selenium.webdriver.Chrome(executable_path=os.path.join(os.path.abspath('./data_management/'), 'chromedriver'),
                                            chrome_options=chrome_options)
    else:
        raise Exception('Can not distinguish the type of OS!')
    # 无界面模式下默认不是全屏，所以需要设置一下分辨率
    BROWSER.set_window_size(1920, 1080)
    WAIT = WebDriverWait(BROWSER, 60, 1)

    # data filter
    FILTER = data_filter.DataFilter()

    def __init__(self):
        # url_dict: keyword-[urls]
        # article_dict: url-(title read like time keywords abstract text segmentation)
        # word_dict: word-(sk-keyword sk-tfidf time idf paper_keyword)
        # simultaneous_dict: word1_2-(sentimes subsentimes)
        self.url_dict = OrderedDict()
        self.article_dict = OrderedDict()
        self.word_dict = OrderedDict()
        self.simultaneous_dict = OrderedDict()
        self.data_file = ''

    def get_data(self, keyword):
        raise Exception('Please implement this method first!')

    def load_data(self):
        print('Loading data file:{}'.format(self.data_file))
        assert self.data_file != '', 'Data filename can not be none!'
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as fin:
                result = pickle.load(fin)
                self.url_dict = result['url_dict']
                self.article_dict = result['article_dict']
                self.word_dict = result['word_dict']
                self.simultaneous_dict = result['simultaneous_dict']
            return True
        else:
            return False

    def save_data(self):
        print('Saving data file:{}'.format(self.data_file))
        assert self.data_file != '', 'Data filename can not be none!'
        data_dir = os.path.dirname(self.data_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        if os.path.exists(self.data_file):
            logging.warn('Data file: \'{}\' already exist and it will be replaced!')

        with open(self.data_file, 'wb') as fout:
            result = {'url_dict': self.url_dict, 'article_dict': self.article_dict,
                      'word_dict': self.word_dict, 'simultaneous_dict': self.simultaneous_dict}
            pickle.dump(result, fout)

        with open(os.path.join(data_dir, 'url_dict.txt'), 'wt', encoding='utf-8') as fout:
            fout.write('# article number ' + '#' * 30 + '\n')
            _urls = set()
            for k, v in self.url_dict.items():
                fout.write('{}: {}\n'.format(k, len(v)))
                _urls = _urls.union(v)
            fout.write('no repeat article number: {}\n'.format(len(_urls)))
            fout.write('\n')
            for k, v in self.url_dict.items():
                fout.write('# {} '.format(k) + '#' * 30 + '\n')
                for i, _url in enumerate(v):
                    fout.write('{}. {}\n'.format(i + 1, _url))
            fout.write('\n')

        with open(os.path.join(data_dir, 'article_dict.txt'), 'wt', encoding='utf-8') as fout:
            # title read like time keywords abstract text segmentation
            for i, (k, v) in enumerate(self.article_dict.items()):
                fout.write('# {} '.format(i + 1) + '#' * 30 + '\n')
                fout.write('url: {}\n'.format(k))
                fout.write('title: {}\n'.format(v[0]))
                fout.write('read: {}\n'.format(v[0]))
                fout.write('like: {}\n'.format(v[0]))
                fout.write('time: {}\n'.format(v[0]))
                fout.write('keywords: {}\n'.format(v[0]))
                fout.write('abstract: {}\n'.format(v[0]))
                fout.write('text: {}\n'.format(v[0]))
                fout.write('segmentation: {}\n\n'.format(v[0]))

        with open(os.path.join(data_dir, 'word_dict.txt'), 'wt', encoding='utf-8') as fout:
            # sk-keyword sk-tfidf time idf paper_keyword
            fout.write('{:20},{:20},{:20},{:20},{:20},{:20}\n'.format('word', 'is_sk_keyword', 'sk_tfidf', 'number',
                                                                      'article_number', 'is_paper_keyword'))
            for k, v in self.word_dict.items():
                fout.write('{:20},{:20},{:20},{:20},{:20},{:20}\n'.format(k, v[0], v[1], v[2], v[3], v[4], v[5]))
        with open(os.path.join(data_dir, 'simultaneous_dict.txt'), 'wt', encoding='utf-8') as fout:
            fout.write('{:60},{:20}\n'.format('word1-word2', 'number'))
            for k, v in self.simultaneous_dict.items():
                fout.write('{:60},{:20}\n'.format(k, v))
