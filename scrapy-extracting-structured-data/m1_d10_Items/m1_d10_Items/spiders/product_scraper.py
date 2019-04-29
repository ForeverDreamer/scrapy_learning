import scrapy
from m1_d10_Items.items import ProductItem

USDINR = 68.0

class ProductDetails(scrapy.Spider):
    name  = 'amazon_product_scraper'

    start_urls = ['https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=macbook']

    def parse(self, response):

            
        titles = response.css('.s-access-title::text').extract()
        links = response.css('a.s-access-detail-page::attr(href)').extract()
        prices = response.css('.s-price::text').extract()

        # 
        truncated_titles = map(lambda title: title[:50], titles)

        product_ids = map(lambda link: link.split('/')[-1], links)
        short_links = map(lambda product_id: 'https://amazon.in/dp/' + product_id, product_ids)

        usd_prices = map(lambda price: float(price.replace(',', '')) / USDINR, prices)

       
        productItem = ProductItem()

        productItem['titles'] = list(truncated_titles)
        productItem['links'] = list(short_links)
        productItem['prices'] = list(usd_prices)
        
        #print('\nProduct title: ', productItem['title'])
        #print('Product link: ', productItem['link'])
        #print('Product price: ', productItem['price'], '\n')

        yield productItem
