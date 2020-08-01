# -*- coding: utf-8 -*-
# @Time   : 2020/7/24 12:29
# @Author : zihaolalala
# @Email  : zihaolalala@163.com
# @File   : testz.py
# @Desc   : 

from LAC import LAC
import jieba

# 装载分词模型
lac = LAC()

# 单个样本输入，输入为Unicode编码的字符串
text = u"LAC是个优秀的分词工具，我经常使用它"
seg_result = lac.run(text)
print(seg_result)
print(jieba.lcut(text))

# 批量样本输入, 输入为多个句子组成的list，平均速率会更快
texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司"]
seg_result = lac.run(texts)
print(seg_result)

pass
