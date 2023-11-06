# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: ua
@time: 2023/10/30 14:22
"""
import requests, os
from fake_useragent import UserAgent

url = 'https://www.sogou.com/web'
word = input('enter a word:')
param = {
    'query': word
}

headers = {
    'User-Agent': UserAgent().random
}
res = requests.get(url=url, params=param, headers=headers)
print(res.request.headers)
# print(res.text)
html = res.text
file_name = word + '.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(html)
if os.path.exists(file_name):
    print('爬取结束')
