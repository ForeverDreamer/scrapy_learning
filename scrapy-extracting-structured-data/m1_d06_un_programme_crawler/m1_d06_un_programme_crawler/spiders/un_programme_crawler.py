from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# Navigate to http://www.un.org/en/sections/about-un/funds-programmes-specialized-agencies-and-others/index.html
# Right-click on one of the programme names (e.g. UNICEF) and inspect the element
# Note that the programme name can be extracted with this selector: div.field-item.even > h4::text
class GenSpiderCrawl(CrawlSpider):

    name = 'un_programme_crawler'
    
    allowed_domains = ['un.org']
    start_urls = ['http://www.un.org/en/sections/about-un/funds-programmes-specialized-agencies-and-others/index.html']

    # first show without allow and deny
    # then show with allow and no deny
    # then allow + deny

    # LinkExtractor will visit all links on the given page and extract all data which matches our selector
    # The first run will scrape everything matching the div.field-item.even > h4::text from all these linked pages
    # rules = (Rule(LinkExtractor(), callback='parse_page'),)

    # Rather than visiting all links on the page, 
    # we restrict to those which contain 'funds-programmes-specialized-agencies-and-others' in the URL
    # This restricts the scraped content to just the specialized agencies, but across all 6 UN languages
    # rules = (Rule(LinkExtractor(allow=('funds-programmes-specialized-agencies-and-others')),callback='parse_page'),)

    # We restrict the extracted links to just 3 languages
    # We block the Chinese, French and Russian pages with the deny rule
    # Only Spanish, Arabic and English 
    rules = (
        Rule(
            LinkExtractor(
                allow='funds-programmes-specialized-agencies-and-others',
                deny=('zh/sections', 'fr/sections', 'ru/sections')
            ),
            callback='parse_page'
        ),
    )

    def parse_page(self, response):

        # Extract the list of agencies using the specified selector
        list_of_agencies = response.css('div.field-item.even > h4::text').extract()
        
        # Write out the list of agencies extracted to a file
        for agency in list_of_agencies:
            with open('un_agencies.txt', 'a+', encoding='utf-8') as f:
                f.write(agency + '\n')




