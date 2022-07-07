from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as ec  # available since 2.26.0
from bs4 import BeautifulSoup
import re
import random
from Util.user_agents import ua_list
import traceback

cookie_dict = {
    # 'checkcode':r'$2a$10$9FVE.1nXJKq/F.nH62OhCevrCqs4skby2bC4IO6VPJITlc7Sh.NZa',
    'c_c':r'a153f80493f411e3801452540a3121f7',
    '_ga':r'GA1.2.1063404131.1384259893',
    'zata':r'zhihu.com.021715f934634a988abbd3f1f7f31f37.470330',
    'q_c1':r'59c45c60a48d4a5f9a12a52028a9aee7|1400081868000|1400081868000',
    '_xsrf':r'2a7cf7208bf24dbda3f70d953e948135',
    'q_c0':r'"NmE0NzBjZTdmZGI4Yzg3ZWE0NjhkNjkwZGNiZTNiN2F8V2FhRTQ1QklrRjNjNGhMdQ==|1400082425|a801fc83ab07cb92236a75c87de58dcf3fa15cff"',
    '__utma':r'51854390.1063404131.1384259893.1400518549.1400522270.5',
    '__utmb':r'51854390.4.10.1400522270',
    '__utmc':r'51854390',
    '__utmz':r'51854390.1400513283.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/hallson',
    '__utmv':r'51854390.100-1|2=registration_date=20121016=1^3=entry_date=20121016=1'
}

URL = "http://www.baidu.com"
# URL = "http://crawleruniverse.com:8000/ct/ri"

try:
    # 设置参数选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    proxy_ip = "186.24.11.165:8080"
    user_agent = random.choice(ua_list)
    # chrome_options.add_argument('--proxy-server=' + proxy_ip)
    chrome_options.add_argument("--user-agent=" + user_agent)
    driver = webdriver.Chrome(options=chrome_options)

    # 应该不需要设置cookies，本身就是浏览器，访问网站时服务器写入的cookies都保存在Chrome Webdriver进程中，
    # 可以通过driver.get_cookies()获取，再次访问该网站时也会自动发送给服务器
    # for name, value in cookie_dict.items():
    #     driver.add_cookie({'name': name, 'value': value})

    driver.get(URL)
    # page_source = driver.page_source
    # soup = BeautifulSoup(page_source, features='lxml')
    #
    # http_x_forwarded_for = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h4")))
    # remote_addr = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h5")))[0]
    # proxy_ip = proxy_ip.split(':')[0]
    # print('http_x_forwarded_for: {}, remote_addr: {}, proxy_ip: {}, pass: {}'.format(http_x_forwarded_for,
    #                                                                                  remote_addr,
    #                                                                                  proxy_ip,
    #                                                                                  proxy_ip == remote_addr))
    # print(soup.find('div').get_text())
    # print(soup.find('span').get_text())
    print('response cookies: ')
    print(driver.get_cookies())
except Exception as e:
    traceback.print_exc()
finally:
    driver.close()

