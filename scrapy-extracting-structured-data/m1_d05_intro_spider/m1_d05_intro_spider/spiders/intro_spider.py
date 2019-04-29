import scrapy

filename = 'book_titles.txt'


class IntroSpider(scrapy.Spider):
    name = "intro_spider"

    # The first request to perform is defined in the start_requests method
    # This is what is called when the Spider is first executed
    # Here we define the list of URLs for which to make requests
    # We also specify the callback function to do the actual parsing
    def start_requests(self):

        # We scrape the first 5 pages of books to scrape
        urls = [
            'http://books.toscrape.com/catalogue/page-1.html',
            'http://books.toscrape.com/catalogue/page-2.html',
            'http://books.toscrape.com/catalogue/page-3.html',
            'http://books.toscrape.com/catalogue/page-4.html',
            'http://books.toscrape.com/catalogue/page-5.html',
        ]

        # We generate a Request for each URL
        # We also specify the use of the parse function to parse the responses
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Define how to handle the response object in the parse function
    # Here, we extract the book titles and write it to a file        
    def parse(self, response):
        
        # Extract the list of book titles into a list
        book_list = response.css('article.product_pod > h3 > a::attr(title)').extract()
        
        with open(filename, 'a+') as f:
            for book_title in book_list:
                f.write(book_title + "\n")
