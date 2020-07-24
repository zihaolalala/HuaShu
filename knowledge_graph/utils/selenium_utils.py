# -*- coding: utf-8 -*-
# @Time   : 2020/7/4 14:26
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : selenium_utils.py
# @Desc   : 

from selenium.webdriver.support.wait import WebDriverWait
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from tqdm import tqdm
from knowledge_graph.data_management import data_loader
from knowledge_graph.utils.log_utils import log_print
import sys


def time_out_tips(seconds):
    for _ in tqdm(range(seconds), '超时失败，{}秒后重试'.format(seconds)):
        time.sleep(1)


def wait_for_elem(xpath, time_out_internals=[60, 120, 180]):
    time_out_nums = 0
    while True:
        try:
            data_loader.DataLoader.WAIT.until(lambda brows: brows.find_element_by_xpath(xpath))
            time.sleep(random.randint(1, 5))
            return True, 1
        except TimeoutException:
            if time_out_nums >= 3:
                return False, -1
            else:
                time_out_tips(time_out_internals[time_out_nums])
                time_out_nums += 1
                continue
        except NoSuchElementException:
            return False, -2
        except Exception as msg:
            log_print(msg)
            return False, -3
