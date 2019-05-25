#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime, timedelta
from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
import fetch_free_proxyes
import requests
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class HttpProxyMiddleware(object):
    # 遇到这些类型的错误直接当做代理不可用处理掉, 不再传给retrymiddleware
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)

    def __init__(self, settings):
        # 保存上次不用代理直接连接的时间点
        self.last_no_proxy_time = datetime.now()
        # 一定分钟数后切换回不用代理, 因为用代理影响到速度
        self.recover_interval = 20
        # 一个proxy如果没用到这个数字就被发现老是超时, 则永久移除该proxy. 设为0则不会修改代理文件.
        self.dump_count_threshold = 20
        # 存放代理列表的文件, 每行一个代理, 格式为ip:port, 注意没有http://, 而且这个文件会被修改, 注意备份
        self.proxy_file = os.path.dirname(os.path.abspath(__file__))+'\\proxies.txt'
        # 是否在超时的情况下禁用代理
        self.invalid_proxy_flag = True
        # 当有效代理小于这个数时(包括直连), 从网上抓取新的代理, 可以将这个数设为为了满足每个ip被要求输入验证码后得到足够休息时间所需要的代理数
        # 例如爬虫在十个可用代理之间切换时, 每个ip经过数分钟才再一次轮到自己, 这样就能get一些请求而不用输入验证码.
        # 如果这个数过小, 例如两个, 爬虫用A ip爬了没几个就被ban, 换了一个又爬了没几次就被ban, 这样整个爬虫就会处于一种忙等待的状态, 影响效率
        self.extend_proxy_threshold = 10
        # 初始化代理列表
        self.proxyes = [{"proxy": None, "valid": True, "count": 0}]
        # 初始时使用0号代理(即无代理)
        self.proxy_index = 0
        # 表示可信代理的数量(如自己搭建的HTTP代理)+1(不用代理直接连接)
        self.fixed_proxy = len(self.proxyes)
        # 上一次抓新代理的时间
        self.last_fetch_proxy_time = datetime.now()
        # 每隔固定时间强制抓取新代理(min)
        self.fetch_proxy_interval = 120
        # 一个将被设为invalid的代理如果已经成功爬取大于这个参数的页面， 将不会被invalid
        self.invalid_proxy_threshold = 200
        # 从文件读取初始代理
        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, "r") as fd:
                lines = fd.readlines()
                for line in lines:
                    line = line.strip()
                    self.proxyes.append({"proxy": line, "valid": True, "count": 0})

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def validUsefulProxy(self, proxy):
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
            print(e)

        logger.info("代理ip已经失效： 重试中...")
        return False

    def set_proxy(self, request):
        """
        将request设置使用为当前的或下一个有效代理
        """
        fetch_url = "http://127.0.0.1:5010/get/"
        proxy = requests.get(url=fetch_url).text
        while not self.validUsefulProxy(proxy):
            proxy = requests.get(url=fetch_url).text

        if not proxy or proxy == 'no proxy!':
            logger.info("set_proxy fail： no available ip")
            del request.meta["change_proxy"]
            return

        prot, ip, port = proxy.split(':')
        proxy = '{}://{}:{}'.format(prot, ip, port)
        logger.info("set_proxy success： proxy is {}".format(proxy))
        request.meta["proxy"] = proxy

    def process_request(self, request, spider):
        """
        将request设置为使用代理
        """
        if datetime.now() > (self.last_no_proxy_time + timedelta(minutes=self.recover_interval)):
            logger.info("After %d minutes later, recover from using proxy" % self.recover_interval)
            self.last_no_proxy_time = datetime.now()

        request.meta["dont_redirect"] = True  # 有些代理会把请求重定向到一个莫名其妙的地址

        # spider发现parse error, 要求更换代理
        if "change_proxy" in request.meta.keys() and request.meta["change_proxy"]:
            logger.info("process_request： change proxy by request: %s" % request)
            request.meta["change_proxy"] = False
            self.set_proxy(request)

    def process_response(self, request, response, spider):
        """
        检查response.status, 根据status是否在允许的状态码中决定是否切换到下一个proxy, 或者禁用proxy
        """
        if "proxy" in request.meta.keys():
            logger.debug("process_response: proxy: {}, status: {}, url: {}".format(request.meta["proxy"], response.status, request.url))
        else:
            logger.debug("process_response: proxy: None, status: {}, url: {}".format(response.status, request.url))

        # status不是正常的200而且不在spider声明的正常爬取过程中可能出现的
        # status列表中, 则认为代理无效, 切换代理
        if response.status != 200 \
                and (not hasattr(spider, "website_possible_httpstatus_list")
                     or response.status not in spider.website_possible_httpstatus_list):
            logger.info("process_response：status not in spider.website_possible_httpstatus_list")
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        else:
            return response

    def process_exception(self, request, exception, spider):
        """
        处理由于使用代理导致的连接异常
        """
        if "proxy" in request.meta.keys():
            logger.debug("process_exception: proxy: {}, exception: {}".format(request.meta["proxy"], exception))
        else:
            logger.debug("process_exception: proxy: None, exception: {}".format(exception))

        new_request = request.copy()
        new_request.meta["change_proxy"] = True
        request.meta["proxy"] = None
        new_request.dont_filter = True
        return new_request
