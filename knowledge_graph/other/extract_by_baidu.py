# -*- coding: utf-8 -*-
# @Time   : 2020/7/7 11:00
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : extract_by_baidu.py
# @Desc   : 

import time
import selenium.webdriver
import urllib.parse
from knowledge_graph.utils.selenium_utils import wait_for_elem
from selenium.webdriver.chrome.options import Options
import re
import os
import pickle
from collections import OrderedDict

# 定义规则
# 关系类别
pattern_str_dict = dict()
pattern_str_dict['继承关系'] = []
pattern_str_dict['整体部分关系'] = []
pattern_str_dict['其他关系'] = []
# 具体关系
pattern_str_dict['继承关系'].append('({}(属于|是)(一.)?[^,.，。！!]*?{})')
pattern_str_dict['继承关系'].append('({}这.?{})')
pattern_str_dict['整体部分关系'].append('{}由[^.,，。！]*{}[^.,，。！]*[组构]成')
pattern_str_dict['整体部分关系'].append('{}包[括含][^.,，。！]*{}[^.,，。！]*')
# pattern_str_dict['其他关系'].append('({}(发生|出现){})')
# pattern_str_dict['其他关系'].append('({}[^.,，。、!！ _\t\s]+{})')


def relation_match(text):
    for k, v in pattern_str_dict.items():
        for _v in v:
            pattern = re.compile(_v.format(word1, word2))
            res = pattern.findall(text)
            if res:
                return True, '{}: {}-{}, {}'.format(k, word1, word2, res)
    return False, None


chrome_options = Options()
chrome_options.add_argument('--headless')
browser = selenium.webdriver.Chrome(executable_path='../CrawlingData/chromedriver.exe',
                                    options=chrome_options)


def get_relation(word1, word2, p_start=0, p_end=3):
    page_file = 'page_{}_{}_{}_{}.pkl'.format(word1, word2, p_start, p_end)
    if not os.path.exists(page_file):
        # recursion_level = 1
        pages = []
        for i in range(p_start, p_end):
            url = 'https://www.baidu.com/s?wd={}&pn={}'
            url = url.format(urllib.parse.quote('{} {}'.format(word1, word2)), i * 10)
            browser.get(url)
            time.sleep(0.5)
            # title_x_path = '//div[@id="content_left"]//div[contains(@class, "c-container")]//h3[contains(@class, "t")]/a'
            # text_x_path = '//div[@id="content_left"]//div[contains(@class, "c-container")]//div[contains(@class, "c-abstract")]'
            abstracts = []
            if wait_for_elem(browser, 30, '//div[@id="content_left"]//div[contains(@class, "c-container")]'):
                bases = browser.find_elements_by_xpath(
                    '//div[@id="content_left"]//div[contains(@class, "c-container")]')
                print('page:{}, len:{}'.format(i + 1, len(bases)))
                for base in bases:
                    # print(base)
                    # 提取url
                    abstract = {}
                    tmp = None
                    try:
                        tmp = base.find_element_by_xpath('.//h3/a')
                        print(tmp.text, ' ', tmp.get_attribute('href'))
                        abstract['url'] = tmp.get_attribute('href')
                        abstract['title'] = tmp.text
                    except Exception:
                        # print(None)
                        pass
                    if tmp is None:
                        tmp = base.find_elements_by_xpath('.//a')
                        # 去除重复的url
                        tmp_urls = set()
                        tmp_urls.union([_tmp.get_attribute('href') for _tmp in tmp])
                        for j in range(len(tmp)):
                            _href = tmp[j].get_attribute('href')
                            if _href in tmp_urls:
                                tmp_urls.remove(_href)
                            else:
                                tmp[j] = None
                        # 去除无关url
                        for _ in tmp:
                            if _ is None:
                                continue
                            if (word1 in _.text) or (word2 in _.text):
                                abstract['url'] = _.get_attribute('href')
                                abstract['title'] = _.text
                                print(_.text, ' ', _.get_attribute('href'))
                                break
                    # 提取text
                    x_paths = ['.//div[contains(@class, "c-abstract")]', './/div[contains(@class, "c-span18")]/p',
                               './/div[contains(@class, "c-span18")]/font', './/div[contains(@class, "c-offset")]',
                               './/div[contains(@class, "c-abstract")]/p', './/div[contains(@class, "c-span24")]/p']
                    for x_path in x_paths:
                        try:
                            _tmp = base.find_element_by_xpath(x_path)
                            abstract['text'] = _tmp.text
                            print(_tmp.text)
                            break
                        except Exception:
                            continue

                    abstracts.append(abstract)

                    # 抽取关系
                    find, result = relation_match(abstract.get('text', ''))
                    find2, result2 = relation_match(abstract.get('title', ''))
                    if find:
                        pages.append(abstracts)
                        with open(page_file, 'wb') as fout:
                            pickle.dump(pages, fout)
                        with open(os.path.basename(page_file) + '.txt', 'wt', encoding='utf-8') as fout:
                            fout.write('Search pages:{}, {}\n'.format(i + 1, result))
                        return result
                    if find2:
                        pages.append(abstracts)
                        with open(page_file, 'wb') as fout:
                            pickle.dump(pages, fout)
                        with open(os.path.basename(page_file) + '.txt', 'wt', encoding='utf-8') as fout:
                            fout.write('Search pages:{}, {}\n'.format(i + 1, result2))
                        return result2
                    print('#' * 50 + '\n')

            pages.append(abstracts)
        with open(page_file, 'wb') as fout:
            pickle.dump(pages, fout)
        with open(os.path.basename(page_file) + '.txt', 'wt', encoding='utf-8') as fout:
            fout.write('Search pages:{}, None\n'.format(p_end))
        return None
    else:
        with open(page_file, 'rb') as fin:
            pages = pickle.load(fin)
        with open(os.path.basename(page_file) + '.txt', 'rt', encoding='utf-8') as fin:
            result = list(fin)[0]
    return result


if __name__ == '__main__':
    # 获取关键词词典
    res = '..\\StatisticAnalysis\\result2.pkl'
    with open(res, 'rb') as fin:
        res = pickle.load(fin)
    # print(type(res))
    print(res.keys())
    text_dict, time_dict = res['keyword_text_dict'], res['keyword_time_dict']
    # 根据关键词语的出现次数确定重要性
    time_dict = OrderedDict(time_dict)
    word_list, time_list = [], []
    for k, v in time_dict.items():
        word_list.append(k)
        time_list.append(v)
    relation_num = [[''] * len(word_list)] * len(word_list)
    for i in range(200):
        for j in range(i + 1, i + 201):
            word1, word2 = word_list[i], word_list[j]
            result = get_relation(word1, word2, p_end=100)
            relation_num[i][j] = result
    print('Finish!')
