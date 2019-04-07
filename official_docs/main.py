# -*- coding: utf-8 -*-
from scrapy import cmdline

cmdline.execute("scrapy crawl scrapy_tutorial -o scrapy_tutorial.jl -a tag=humor".split())
