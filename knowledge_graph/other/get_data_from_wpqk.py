# -*- coding: utf-8 -*-
# @Time   : 2020/7/21 11:33
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : get_data_from_wpqk.py
# @Desc   : 

import selenium.common
import selenium.webdriver
import urllib.parse
import time
import pickle
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime
import logging
import random

if __name__ == '__main__':
    data_dir = 'data/'
# 创建工作目录
work_dir = os.path.join('data', str(datetime.now()).replace(':', '-').replace(' ', '-'))
if not os.path.exists(work_dir):
    os.makedirs(work_dir)

# 设置日志文件
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_file = open(os.path.join(work_dir, 'stdout.txt'), 'wt', encoding='utf-8')
handler = logging.StreamHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# 设置chrome浏览器无界面模式
chrome_options = Options()
chrome_options.add_argument('--headless')
browser = selenium.webdriver.Chrome(executable_path='../data_management/chromedriver.exe', chrome_options=chrome_options)
# 无界面模式下默认不是全屏，所以需要设置一下分辨率
browser.set_window_size(1920, 1080)
wait = WebDriverWait(browser, 30, 1)


def my_print(content):
    print(content)
    logger.info(content)


def time_out_tips():
    for _ in tqdm(range(30), '超时失败，30秒后重试'):
        time.sleep(1)


def get_urls(keywords):
    url_dict = dict()  # 结果集
    base_url = 'https://www.jianshu.com/search?q={}&page={}&type=note'

    def wait_for_elem(xpath):
        time_out_nums = 0
        while True:
            try:
                wait.until(lambda browser: browser.find_element_by_xpath(xpath))
                time.sleep(random.randint(1, 5))
                return True
            except selenium.common.exceptions.TimeoutException:
                if time_out_nums >= 3:
                    return None, -1
                else:
                    time_out_nums += 1
                    time_out_tips()
                    continue

    def get_current_page_urls():
        if wait_for_elem('//ul[@class="note-list"]'):
            note_elems = []
            urls, absts = [], []
            try:
                note_list = browser.find_element_by_xpath('//ul[@class="note-list"]')
                note_elems = note_list.find_elements_by_css_selector('li > div.content > a')
                # my_print(len(note_elems))
            except selenium.common.exceptions.NoSuchElementException:
                pass
            for elem in note_elems:
                urls.append(elem.get_attribute('href'))
                absts.append(elem.text)
            return urls, absts

    for i, keyword in enumerate(keywords):
        url_dict[keyword] = {'has_search_page': 0, 'urls': list(), 'absts': list()}
        for page in range(1, 2):
            my_print('keyword:{}, Searching page:{}...'.format(keyword, page))
            url = base_url.format(urllib.parse.quote(keyword), page)
            # 发送请求
            browser.get(url)
            # 页面滚动，直至出现”下一页“链接，或超时没出现，或本来就没有
            # driver.execute_script('document.documentElement.scrollTop=5000')
            # 获取当前页文章
            urls, absts = get_current_page_urls()
            url_dict[keyword]['has_search_page'] = page
            url_dict[keyword]['urls'].extend(urls)
            url_dict[keyword]['absts'].extend(absts)
            if len(urls) < 10:
                break
    return url_dict


if __name__ == '__main__':
    keywords = ['故障', '天文学']
    urls = get_urls(keywords)

    # 保存到本地
    with open(os.path.join(work_dir, 'bin_data.pkl'), 'wb') as fout:
        pickle.dump(urls, fout)
    for k, v in urls.items():
        with open(os.path.join(work_dir, '{}.txt'.format(k)), 'wt', encoding='utf-8') as fout:
            fout.write('has_search_page:{}\n'.format(v['has_search_page']))
            nums = len(v['urls'])
            for i in range(nums):
                fout.write('{} # {}\n'.format(v['urls'][i], v['absts'][i]))
    my_print('Finish!')
    log_file.close()
