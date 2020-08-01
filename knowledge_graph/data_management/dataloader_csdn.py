# -*- coding: utf-8 -*-
# @Time   : 2020/7/23 9:21
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : dataloader_csdn.py
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


class CsdnDataLoader(DataLoader):

    def __init__(self, work_dir):
        super().__init__()
        self.work_dir = os.path.join(work_dir, 'csdn')

    def get_url_articl(self, keywords, pages=15):
        log_print('Geting urls from csdn...')
        # self.url_dict: keyword-[urls]
        base_url = 'https://so.csdn.net/so/search/s.do?p={}&q={}&t=blog&viparticle=&domain=&o=&s=&u=&l=&f=&rbg=0'

        def get_absts_page():
            # 获取url和标题
            urls, titles, absts = [], [], []
            if wait_for_elem('//div[@class="search-list-con"]/dl[contains(@class, "search-list")]'):
                try:
                    # title read like time keywords abstract text segmentation
                    node_list = DataLoader.BROWSER.find_elements_by_xpath('//div[@class="search-list-con"]/dl[contains(@class, "search-list")]')
                    for node in node_list:
                        try:
                            tmp1 = node.find_element_by_css_selector('dt > div.limit_width > a')
                            tmp2 = node.find_element_by_css_selector('dd.search-detail')
                            if DataLoader.FILTER.filter_when_getting(keyword, tmp1.text, tmp2.text):
                                urls.append(tmp1.get_attribute('href'))
                                titles.append(tmp1.text)
                                absts.append(tmp2.text)
                        except selenium.common.exceptions.NoSuchElementException:
                            continue
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
            read_nums_, like_ = 0, 0
            if wait_for_elem('//div[@id="content_views"]'):
                try:
                    article = DataLoader.BROWSER.find_element_by_xpath('//div[@id="content_views"]')
                    art_time = DataLoader.BROWSER.find_element_by_xpath('//div[@class="bar-content"]/span[@class="time"]')
                    read_nums = DataLoader.BROWSER.find_element_by_xpath('//div[@class="bar-content"]/span[@class="read-count"]')
                    like = DataLoader.BROWSER.find_element_by_xpath('//div[@class="bar-content"]/a/span[@class="get-collection"]')
                    log_print('article:{}'.format(article.text))
                    log_print(art_time.text)
                    log_print(read_nums.text)
                    log_print(like.text)
                except selenium.common.exceptions.NoSuchElementException:
                    log_print('NoSuchElementException!')
                    return []
                except selenium.common.exceptions.TimeoutException:
                    log_print('TimeoutException!')
                    return []
                except Exception as msg:
                    log_print(msg)
                    return []

                if read_nums.text.replace(' ', '') != '':
                    read_nums_ = int(read_nums.text.replace(' ', ''))
                if like.text.replace(' ', '') != '':
                    like_ = int(like.text.replace(' ', ''))
                result = ['', read_nums_, like_, art_time.text, [], '', article.text, None]
            return result

        try:
            for i, keyword in enumerate(keywords):
                self.url_dict[keyword] = set()
                for page in range(1, pages + 1):
                    log_print('keyword:{}, Searching page:{}...'.format(keyword, page))
                    url = base_url.format(page, urllib.parse.quote(keyword))
                    # 发送请求
                    DataLoader.BROWSER.get(url)
                    # 页面滚动，直至出现”下一页“链接，或超时没出现，或本来就没有
                    # driver.execute_script('document.documentElement.scrollTop=5000')
                    # 获取当前页文章
                    urls, titles, absts = get_absts_page()
                    for url, title, abst in zip(urls, titles, absts):
                        if url not in self.article_dict.keys():
                            log_print(title)
                            result = get_article(url)
                            if len(result) > 0:
                                result[0] = title
                                self.article_dict[url] = result
                        if (url in self.article_dict) and (url not in self.url_dict[keyword]):
                            self.url_dict[keyword].add(url)
                    if len(urls) < 5:
                        break
        except InterruptedError:
            log_print('Stop manually!')
        finally:
            self.save_url_articl()
