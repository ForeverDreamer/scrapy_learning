from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as ec  # available since 2.26.0
from bs4 import BeautifulSoup
import re
import random
import traceback
from user_agents import ua_list

headers = {
            # "Host": "www.zhihu.com",
            'User-Agent': random.choice(ua_list),
            # "Referer": "http://www.zhihu.com/people/raymond-wang",
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

URL = "https://www.youtube.com/watch?v=biqYLYJZgEM&list=PLWIBmxdTr81dDEZRiNxoy55dIDWtMyOoc&index=1"  # 查自己的ip

try:
    # 设置参数选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = random.choice(ua_list)
    chrome_options.add_argument("--user-agent=" + user_agent)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    WebDriverWait(driver, 30).until(ec.title_contains("Appium Python Tutorial - Python and Pycharm Installation - YouTube"))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features='lxml')
    HOST = 'https://www.youtube.com'
    TARGET_FILE = 'links.txt'
    link_list = sorted(set(re.findall(r'href="(/watch\?[\s\S]*?index=\d+)', page_source)),
                       key=lambda index: int(re.findall(r'index=(\d+)', index)[0]))
    with open(TARGET_FILE, 'wt') as fw:
        for item in link_list:
            sub_item = re.sub(r'&amp;', '&', item)
            fw.write(HOST + sub_item.strip() + "\n")
except Exception as e:
    traceback.print_exc()
finally:
    driver.close()