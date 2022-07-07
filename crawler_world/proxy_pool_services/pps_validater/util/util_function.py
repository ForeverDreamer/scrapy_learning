# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、get_html_soup
-------------------------------------------------
"""
import requests
import re
from bs4 import BeautifulSoup
from .log_handler import LogHandler

logger = LogHandler(__name__, stream=False)


def valid_useful_proxy(proxy):
    url = "http://crawleruniverse.com:8000/ct/ri"  # 查自己的ip
    prot, ip, port = proxy.split(':')

    try:
        proxies = {
            prot: '{}://{}:{}'.format(prot, ip, port)
        }
        r = requests.get(url, proxies=proxies, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, 'lxml')

        http_x_forwarded_for = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h4")))
        remote_addr = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h5")))[0]
        if ip == remote_addr:
            print('http_x_forwarded_for: {}, remote_addr: {}, ip: {}, pass: {}'.format(http_x_forwarded_for,
                                                                                       remote_addr,
                                                                                       ip,
                                                                                       ip == remote_addr))
            return True
    except Exception as e:
        # pass
        logger.error(e)

    return False
