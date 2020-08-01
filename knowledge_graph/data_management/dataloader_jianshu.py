# -*- coding: utf-8 -*-
# @Time   : 2020/7/23 9:21
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : dataloader_jianshu.py
# @Desc   : 

from knowledge_graph.data_management.data_loader import DataLoader
import selenium.common
import selenium.webdriver
import urllib.parse
import time
import pickle
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os
import jieba
from datetime import datetime
import random
from knowledge_graph.utils.selenium_utils import time_out_tips, wait_for_elem
from knowledge_graph.utils.log_utils import log_print
from tqdm import tqdm

# # 创建工作目录
# work_dir = os.path.join('data', str(datetime.now()).replace(':', '-').replace(' ', '-'))
# if not os.path.exists(work_dir):
#     os.makedirs(work_dir)


class JianShuDataLoader(DataLoader):

    def __init__(self, work_dir):
        super().__init__()
        self.word_dir = work_dir
        self.data_file = os.path.join(work_dir, 'jianshu/data.pkl')

    def get_url_articl(self, keywords, pages=100):
        log_print('Geting urls from JianShu...')
        # self.url_dict: keyword-[urls]
        base_url = 'https://www.jianshu.com/search?q={}&page={}&type=note'

        def get_absts_page():
            # 获取url和标题
            urls, titles, absts = [], [], []
            if wait_for_elem('//ul[@class="note-list"]/li/div[@class="content"]'):
                try:
                    # title read like time keywords abstract text segmentation
                    node_list = DataLoader.BROWSER.find_elements_by_xpath(
                        '//ul[@class="note-list"]/li/div[@class="content"]')
                    for node in node_list:
                        tmp1 = node.find_element_by_css_selector('a.title')
                        tmp2 = node.find_element_by_css_selector('p.abstract')
                        if DataLoader.FILTER.filter_when_getting(keyword, tmp1.text, tmp2.text):
                            urls.append(tmp1.get_attribute('href'))
                            titles.append(tmp1.text)
                            absts.append(tmp2.text)
                except selenium.common.exceptions.NoSuchElementException:
                    log_print('NoSuchElementException!')
                    return [], [], []
                except selenium.common.exceptions.TimeoutException:
                    log_print('TimeoutException!')
                    return [], [], []
                except Exception as msg:
                    log_print(msg)
                    return [], [], []
            return urls, titles, absts

        def get_article(url):
            # 获取文章正文
            # article_dict: url-(title read like time keywords abstract text segmentation)
            DataLoader.BROWSER.get(url)
            log_print('Browsing url:{}...'.format(url))
            result = []
            if wait_for_elem('//article[@class="_2rhmJa"]'):
                try:
                    title = DataLoader.BROWSER.find_element_by_xpath('//h1[@class="_1RuRku"]')
                    article = DataLoader.BROWSER.find_element_by_xpath('//article[@class="_2rhmJa"]')
                    dsoj = DataLoader.BROWSER.find_element_by_xpath('//div[@class="s-dsoj"]')
                    art_time = dsoj.find_element_by_xpath('//time')
                    read_nums = dsoj.find_element_by_xpath('//span[contains(text(), "阅读")]')
                    like = DataLoader.BROWSER.find_element_by_xpath('//span[@class="_1LOh_5"]')
                    # log_print('title:{}'.format(title.text))
                    # log_print(art_time.text)
                    # log_print(read_nums.text)
                    # log_print(like.text)
                except selenium.common.exceptions.NoSuchElementException:
                    log_print('NoSuchElementException!')
                    return []
                except selenium.common.exceptions.TimeoutException:
                    log_print('TimeoutException!')
                    return []
                except Exception as msg:
                    log_print(msg)
                    return []
                result = [title.text, int(read_nums.text.replace(',', '').split(' ')[-1]),
                          int(like.text.replace(',', '')[:-3]), art_time.text, [], '', article.text,
                          None]
            return result

        for i, keyword in enumerate(keywords):
            self.url_dict[keyword] = set()
            for page in range(1, pages):
                log_print('keyword:{}, Searching page:{}...'.format(keyword, page))
                url = base_url.format(urllib.parse.quote(keyword), page)
                # 发送请求
                DataLoader.BROWSER.get(url)
                # 页面滚动，直至出现”下一页“链接，或超时没出现，或本来就没有
                # driver.execute_script('document.documentElement.scrollTop=5000')
                # 获取当前页文章
                urls, titles, absts = get_absts_page()
                for url, title, abst in zip(urls, titles, absts):
                    if url not in self.article_dict.keys():
                        result = get_article(url)
                        if len(result) > 0:
                            # result[-3] = abst
                            self.article_dict[url] = result
                    if (url in self.article_dict) and (url not in self.url_dict[keyword]):
                        self.url_dict[keyword].add(url)
                if len(urls) < 10:
                    break
        self.save_url_articl()
