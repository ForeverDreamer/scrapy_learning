# -*- coding: utf-8 -*-

import scrapy


class ScrapyTutorial(scrapy.Spider):
    name = "scrapy_tutorial"

    # example 1

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         # 'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    #
    # def parse(self, response):
    #     # page = response.url.split("/")[-2]
    #     # filename = 'quotes-%s.html' % page
    #     # with open(filename, 'wb') as f:
    #     #     f.write(response.body)
    #     # self.log('Saved file %s' % filename)
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }
    #
    #     # next_page = response.css('li.next a::attr(href)').get()
    #     # if next_page is not None:
    #     #     next_page = response.urljoin(next_page)
    #     #     # yield scrapy.Request(next_page, callback=self.parse)
    #     #     yield response.follow(next_page, callback=self.parse)
    #
    #     # for href in response.css('li.next a::attr(href)'):
    #     #     yield response.follow(href, callback=self.parse)
    #
    #     for a in response.css('li.next a'):
    #         yield response.follow(a, callback=self.parse)

    # example 2

    # start_urls = ['http://quotes.toscrape.com/']

    # def parse(self, response):
    #     # follow links to author pages
    #     for href in response.css('.author + a::attr(href)'):
    #         yield response.follow(href, self.parse_author)
    #
    #     # follow pagination links
    #     for href in response.css('li.next a::attr(href)'):
    #         yield response.follow(href, self.parse)
    #
    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).get(default='').strip()
    #
    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }

    # example 3

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            # url = url + 'tag/' + tag
            # 避免301重定向
            url = url + 'tag/' + tag + '/'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)