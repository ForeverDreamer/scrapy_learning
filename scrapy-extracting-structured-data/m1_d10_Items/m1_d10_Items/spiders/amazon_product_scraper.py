import scrapy
from m1_d10_Items.items import ProductItem

USDINR = 68.0

class ProductDetails(scrapy.Spider):
    name  = 'macbook_scraper'

    start_urls = ['https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=macbook']

    def parse(self, response):

        search_results = response.css('ul.s-result-list > li')

        for product in search_results:
            
            title = product.css('.s-access-title::text').extract_first()
            link = product.css('a.s-access-detail-page::attr(href)').extract_first()
            price = product.css('.s-price::text').extract_first()

            # 
            truncated_title = title[:50]

            product_id = link.split('/')[-1]
            short_link = 'https://amazon.in/dp/' + product_id

            usd_price = float(price.replace(',', '')) / USDINR

           
            productItem = ProductItem()

            productItem['title'] = truncated_title
            productItem['link'] = short_link
            productItem['price'] = usd_price
            
            #print('\nProduct title: ', productItem['title'])
            #print('Product link: ', productItem['link'])
            #print('Product price: ', productItem['price'], '\n')

            yield productItem
