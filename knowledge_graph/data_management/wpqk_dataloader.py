# -*- coding: utf-8 -*-
# @Time   : 2020/7/23 9:21
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : wpqk_dataloader.py
# @Desc   : 

from knowledge_graph.data_management import data_loader
import selenium.common
import selenium.webdriver
import urllib.parse
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime
import logging
import random
from knowledge_graph.utils.selenium_utils import time_out_tips

# 创建工作目录
work_dir = os.path.join('data', str(datetime.now()).replace(':', '-').replace(' ', '-'))
if not os.path.exists(work_dir):
    os.makedirs(work_dir)

# 设置日志文件
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_file = open(os.path.join(work_dir, 'wpqk_stdout.txt'), 'wt', encoding='utf-8')
handler = logging.StreamHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# 设置chrome浏览器无界面模式
chrome_options = Options()
chrome_options.add_argument('--headless')
browser = selenium.webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
# 无界面模式下默认不是全屏，所以需要设置一下分辨率
browser.set_window_size(1920, 1080)
wait = WebDriverWait(browser, 30, 1)


class WPQKDataLoader(data_loader.DataLoader):

    def __init__(self):
        super().__init__()
        self.data_file = 'data/wpqk_data.pkl'

    def load_data(self, keyword):
        def get_urls(keywords):
            url_dict = dict()  # 结果集
            base_url = 'http://qikan.cqvip.com/Qikan/Search/Index?key={}'

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
                if wait_for_elem('//div[@id="articlelist"]'):
                    note_elems = []
                    urls, keywords, absts = [], [], []
                    try:
                        note_list = browser.find_element_by_xpath('//div[@id="articlelist"]')
                        note_elems = note_list.find_elements_by_css_selector('dl')
                        # my_print(len(note_elems))
                    except selenium.common.exceptions.NoSuchElementException:
                        pass
                    for elem in note_elems:
                        urls.append(elem.find_elements_by_css_selector('dt > a').get_attribute('href'))
                        keywords.append(elem.find_elements_by_css_selector('span[@class="subject"]').text)
                        absts.append(elem.find_elements_by_css_selector('span[@class="abstract"]').text)
                    return urls, keywords, absts

            for i, keyword in enumerate(keywords):
                url_dict[keyword] = {'has_search_page': 0, 'urls': list(), 'absts': list(), 'keywords': list()}
                for page in range(1, 20):
                    print('keyword:{}, Searching page:{}...'.format(keyword, page))
                    url = base_url.format(urllib.parse.quote(keyword), page)
                    # 发送请求
                    browser.get(url)
                    # 页面滚动，直至出现”下一页“链接，或超时没出现，或本来就没有
                    # driver.execute_script('document.documentElement.scrollTop=5000')
                    # 获取当前页文章
                    urls, keywords, absts = get_current_page_urls()
                    url_dict[keyword]['has_search_page'] = page
                    url_dict[keyword]['urls'].extend(urls)
                    url_dict[keyword]['absts'].extend(absts)
                    url_dict[keyword]['keywords'].extend(keywords)
                    if len(urls) < 10:
                        break
            return url_dict

        keywords = ['机器人故障']
        urls = get_urls(keywords)

        # 保存到本地
        for k, v in urls.items():
            with open(os.path.join(work_dir, '{}.txt'.format(k)), 'wt', encoding='utf-8') as fout:
                fout.write('has_search_page:{}\n'.format(v['has_search_page']))
                nums = len(v['urls'])
                for i in range(nums):
                    fout.write('{} # {} # {}\n'.format(v['urls'][i], v['absts'][i], v['keywords'][i]))
        print('Finish!')
        log_file.close()
        self.save_data()
        return self.url_dict, self.article_dict, self.word_dict, self.simultaneous_dict


if __name__ == '__main__':
    wpqk_data_loader = WPQKDataLoader()
    data = wpqk_data_loader.load_data('机器故障')
    print(data)
