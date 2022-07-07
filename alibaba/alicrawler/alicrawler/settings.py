# -*- coding: utf-8 -*-

# Scrapy settings for alicrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sys
import random
import django

from shutil import which
from alicrawler.utils.user_agents import ua_list

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'aliserver.settings'
# 手动初始化Django：
django.setup()

USER_AGENTS = ua_list

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
# SELENIUM_DRIVER_ARGUMENTS = ['--headless']
SELENIUM_DRIVER_ARGUMENTS = ['--start-maximized']  # 浏览器窗口最大化
SELENIUM_DRIVER_PROXY = {'enable': False, 'password': False}

BOT_NAME = 'alicrawler'

SPIDER_MODULES = ['alicrawler.spiders']
NEWSPIDER_MODULE = 'alicrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'alicrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "Host": "www.test.com",
#     'User-Agent': random.choice(ua_list),
#     "Referer": "http://www.zhihu.com/people/raymond-wang",
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'Upgrade-Insecure-Requests': '1',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
# }

# ip没有变，User-Agent一直变或格式错误异常(网上拷贝的)有可能被识别为爬虫，测试一下每次请求的response的Cookie用是否需要手动加进去
DEFAULT_REQUEST_HEADERS = {
    'Content-Length': '', 'Content-Type': 'text/plain',
    # 'Host': '127.0.0.1:8000',
    'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Dnt': '1', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7',
    # 'Cookie': 'csrftoken=Wmi8NZmkY7hD3sy0h3EpJXU0owRjtjLlcdx48Tsa70icPIBgXCHwIwiLlCGJNF2P; sessionid=qfejn77jauoiw1mtws2xli0dptgfiwb1'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
# #     'alicrawler.middlewares.AlicrawlerSpiderMiddleware': 543,
# # }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'alicrawler.middlewares.AlicrawlerDownloaderMiddleware': 543,
    # 'alicrawler.middlewares.RandomUserAgentDownloaderMiddleware': 543,
    # 'http_proxy_middleware.http_proxy_middleware.HttpProxyMiddleware': 544,
    'scrapy_selenium.SeleniumMiddleware': 800,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'alicrawler.pipelines.AlicrawlerPipeline': 300,
    'alicrawler.pipelines.TruncateTitle': 100,
    'alicrawler.pipelines.ProductPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOAD_TIMEOUT = 10
