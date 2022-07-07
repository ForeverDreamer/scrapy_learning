# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     WebRequest
   Description :   Network Requests Class
   Author :        J_hao
   date：          2017/7/31
-------------------------------------------------
   Change Activity:
                   2017/7/31:
-------------------------------------------------
"""
__author__ = 'J_hao'

from requests.models import Response
import requests
import random
import time
from .user_agents import ua_list


class WebRequest(object):
    def __init__(self, *args, **kwargs):
        pass

    @property
    def user_agent(self):
        """
        return an User-Agent at random
        :return:
        """
        return random.choice(ua_list)

    @property
    def header(self):
        """
        basic header
        :return:
        """
        return {
            # "Host": "www.zhihu.com",
            'User-Agent': self.user_agent,
            # "Referer": "http://www.zhihu.com/people/raymond-wang",
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

    def get(self, url, proxies, retry_time=5, timeout=30,
            retry_flag=list(), retry_interval=5, **kwargs):
        """
        get method
        :param url: target url
        :param proxies: proxy server
        :param retry_time: retry time when network error
        :param timeout: network timeout
        :param retry_flag: if retry_flag in content. do retry
        :param retry_interval: retry interval(second)
        :param kwargs:
        :return:
        """
        while True:
            try:
                html = requests.get(url, headers=self.header, proxies=proxies, timeout=timeout, **kwargs)
                if any(f in html.content for f in retry_flag):
                    raise Exception
                return html
            except Exception as e:
                print(e)
                retry_time -= 1
                if retry_time <= 0:
                    # 多次请求失败
                    resp = Response()
                    resp.status_code = 200
                    return resp
                time.sleep(retry_interval)
