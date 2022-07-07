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
import time
import re
from bs4 import BeautifulSoup
from .log_handler import LogHandler
from .web_request import WebRequest

logger = LogHandler(__name__, stream=False)


def tcp_connect(proxy):
    """
    TCP 三次握手
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


def robust_crawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("sorry, 抓取出错。错误原因:")
            logger.error(e)

    return decorate


def verify_proxy_format(proxy):
    import re
    verify_regex = r"https?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


def get_html_soup(url, proxy_ip):
    # TODO 取代理服务器用代理服务器访问
    wr = WebRequest()
    # delay 5s for per request
    time.sleep(5)

    # ip, port, prot = proxy_ip.split(':')
    # proxies = {prot: '{}://{}:{}'.format(prot, ip, port)}
    #
    html = wr.get(url, proxies=None).text

    return BeautifulSoup(html, features='lxml')


def extract_ip(ip_info):
    ip = re.findall(r'\d+\.\d+\.\d+\.\d+', ip_info)
    if len(ip) > 0:
        ip = ip[0]

    port = re.findall(r'(\d{4,5})<', ip_info)
    if len(port) > 0:
        port = port[0]

    protocol = re.findall(r'https?|HTTPS?', ip_info)
    if len(protocol) > 0:
        protocol = protocol[0].lower()
    else:
        protocol = 'http'

    return "{}:{}:{}".format(protocol, ip, port)


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
