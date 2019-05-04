# -*- coding: utf-8 -*-
import os
# import sys
# import urllib2
import requests
import re
from lxml import etree


def string_list_save(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))


def page_info(my_page):
    """Regex"""
    mypage_info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a>'
                             r'</div></div>', my_page, re.S)
    return mypage_info


def new_page_info(new_page):
    """Regex(slowly) or Xpath(fast)"""
    # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)">(.*?)</a></td>', new_page, re.S) # bugs
    # results = []
    # for url, item in new_page_Info:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    return zip(new_items, new_urls)


def spider(url):
    i = 0
    print("downloading ", url)
    my_page = requests.get(url).content.decode("gbk")
    # myPage = urllib2.urlopen(url).read().decode("gbk")
    my_page_results = page_info(my_page)
    save_path = u"网易新闻抓取"
    filename = str(i)+"_"+u"新闻排行榜"
    string_list_save(save_path, filename, my_page_results)
    i += 1
    for item, url in my_page_results:
        print("downloading ", url)
        new_page = requests.get(url).content.decode("gbk")
        # new_page = urllib2.urlopen(url).read().decode("gbk")
        new_page_results = new_page_info(new_page)
        filename = str(i)+"_"+item
        string_list_save(save_path, filename, new_page_results)
        i += 1


if __name__ == '__main__':
    print("start")
    start_url = "http://news.163.com/rank/"
    spider(start_url)
    print("end")
