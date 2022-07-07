# import sys
import requests
import random

from util.user_agents import ua_list
from util.util_function import get_html_soup, extract_ip

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as ec  # available since 2.26.0
from bs4 import BeautifulSoup


# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()
# 应该不需要，在主模块执行一次就好
# sys.path.append('..')


class GetFreeProxy(object):
    """
    proxy getter
    """
    @staticmethod
    def get_wuyou(proxy_ip):
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        """
        url_list = [
            'http://www.data5u.com/',
            # 'http://www.data5u.com/free/gngn/index.shtml',
            # 'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        for url in url_list:
            soup = get_html_soup(url, proxy_ip)
            ip_list = soup.find_all('ul', {"class": "l2"})
            for info in ip_list:
                yield extract_ip(str(info))

    @staticmethod
    def get_66ip(proxy_ip):
        base_url = "http://www.66ip.cn/"

        try:
            # 设置参数选项
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            # proxy_ip = "186.24.11.165:8080"
            # ip, port = proxy_ip.split(':')
            # proxy_ip = '{}:{}'.format(ip, port)
            user_agent = random.choice(ua_list)
            # chrome_options.add_argument('--proxy-server=' + proxy_ip)
            chrome_options.add_argument("--user-agent=" + user_agent)

            driver = webdriver.Chrome(options=chrome_options)

            end_page = 200  # 每次只爬取前200页(根据代理质量调整)
            page_num = 1
            while page_num <= end_page:
                driver.get(base_url + str(page_num) + '.html')
                WebDriverWait(driver, 30).until(ec.title_contains("66免费代理ip"))
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, features='lxml')
                ip_list = soup.find_all('tr')
                for info in ip_list:
                    yield extract_ip(str(info))
                page_num += 1
        except Exception as e:
            print(e)
        finally:
            driver.close()

    @staticmethod
    def get_xici(proxy_ip):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        last_page = 200
        page_num = 1
        for url in url_list:
            while page_num <= last_page:
                url = url + str(page_num)
                soup = get_html_soup(url, proxy_ip)
                ip_list = soup.find_all('tr')
                for info in ip_list:
                    yield extract_ip(str(info))
            else:
                # last_page = 729
                page_num = 1


if __name__ == '__main__':
    from util.check_proxy import CheckProxy

    CheckProxy.checkGetProxyFunc(GetFreeProxy.get_wuyou)
    CheckProxy.checkGetProxyFunc(GetFreeProxy.get_66ip)
    CheckProxy.checkGetProxyFunc(GetFreeProxy.get_xici)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyFourth)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyFifth)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxySixth)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxySeventh)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyEight)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyNinth)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyTen)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyEleven)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyTwelve)

    # CheckProxy.checkAllGetProxyFunc()
