import requests
from bs4 import BeautifulSoup
import re

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

url = "http://crawleruniverse.com:8000/ct/ri"  # 查自己的ip
ip, port, prot = '189.196.168.78:30880:http'.split(':')

try:
    proxies = {
        prot: '{}://{}:{}'.format(prot, ip, port)
    }
    r = requests.get(url, proxies=None, cookies=cookie_dict, timeout=10, verify=False)
    soup = BeautifulSoup(r.text, 'lxml')

    http_x_forwarded_for = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h4")))
    remote_addr = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h5")))[0]
    print('http_x_forwarded_for: {}, remote_addr: {}, ip: {}, equal: {}'.format(http_x_forwarded_for,
                                                                                remote_addr,
                                                                                ip,
                                                                                ip == remote_addr))
    print(soup.find('span').get_text())
    print(soup.find('div').get_text())
except Exception as e:
    print(e)
