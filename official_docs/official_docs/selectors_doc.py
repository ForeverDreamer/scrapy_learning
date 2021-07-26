from pprint import pprint as pp

from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests as http

# 1 Using selectors

# 1.1 Constructing selectors
REQUEST_HEADER = {
    'User-agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; iCafeMedia; .NET CLR 2.0.50727; CIBA)',
    'Accept': '*/*',
    'Accept-Charset': 'gzip, deflate',
    # 'Cookie': 'Tango_UserReference=38D8FF1624305B16496E9808; MTCCK=1; _csuid=48feeef505683659; cookmcnt=999; CID=1459382; cookMemberName=YunFan; cookMemberID=61448; savedEmail=liyunfan@genscriptcorp.com; DLDExec=OK; __utma=232384002.1655516880.1231991960.1231994793.1232000250.3; __utmb=232384002; __utmc=232384002; __utmz=232384002.1231991960.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)',
    'Accept-Language': 'en'
}

body = '<html><body><span>good</span></body></html>'
pp(Selector(text=body).xpath('//span/text()').get())

response = HtmlResponse(url='http://example.com', body=body, encoding='utf-8')
pp(Selector(response=response).xpath('//span/text()').get())
print('--------------------------1.1 结束----------------------------')

# 1.2 Using selectors
# body = http.get(url='https://docs.scrapy.org/en/latest/_static/selectors-sample1.html', headers=REQUEST_HEADER).text
body = """
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <a href='#'>Outer tag</a>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>
"""
response = HtmlResponse(
    url='https://docs.scrapy.org/en/latest/_static/selectors-sample1.html',
    body=body,
    encoding='utf-8')
pp(response.xpath('//title/text()'))
pp(response.xpath('//title/text()').getall())
pp(response.xpath('//title/text()').get())
pp(response.css('title::text').get())
pp(response.css('img').xpath('@src').getall())
pp(response.css('a').xpath('@href').getall())
pp(response.xpath('//div[@id="images"]/a/text()').get())
pp(response.xpath('//div[@id="not-exists"]/text()').get() is None)
pp(response.xpath('//div[@id="not-exists"]/text()').get(default='not-found'))
pp([img.attrib['src'] for img in response.css('img')])
pp(response.css('img').attrib['src'])
pp(response.css('base').attrib['href'])
pp(response.xpath('//base/@href').get())
pp(response.css('base::attr(href)').get())
pp(response.css('base').attrib['href'])
pp(response.xpath('//a[contains(@href, "image")]/@href').getall())
pp(response.css('a[href*=image]::attr(href)').getall())
pp(response.xpath('//a[contains(@href, "image")]/img/@src').getall())
pp(response.css('a[href*=image] img::attr(src)').getall())
print('--------------------------1.2 结束----------------------------')

# 1.3 Extensions to CSS Selectors
pp(response.css('title::text').get())
pp(response.css('#images *::text').getall())
pp(response.css('img::text').getall())
pp(response.css('img::text').get() is None)
pp(response.css('img::text').get(default=''))
pp(response.css('a::attr(href)').getall())

print('--------------------------1.3 结束----------------------------')

# 1.4 Nesting selectors
links = response.xpath('//a[contains(@href, "image")]')
pp(links.getall())
for index, link in enumerate(links):
    href_xpath = link.xpath('@href').get()
    img_xpath = link.xpath('img/@src').get()
    print(f'Link number {index} points to url {href_xpath!r} and image {img_xpath!r}')
print('--------------------------1.4 结束----------------------------')

# 1.5 Selecting element attributes
pp(response.xpath("//a/@href").getall())
pp(response.css('a::attr(href)').getall())
pp([a.attrib['href'] for a in response.css('a')])
pp(response.css('base').attrib)
pp(response.css('base').attrib['href'])
pp(response.css('foo').attrib)
print('--------------------------1.5 结束----------------------------')

# 1.6 Using selectors with regular expressions
pp(response.xpath('//a[contains(@href, "image")]/text()'))
pp(response.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)'))
pp(response.xpath('//a[contains(@href, "image")]/text()').re_first(r'Name:\s*(.*)'))
print('--------------------------1.6 结束----------------------------')

# 1.7 extract() and extract_first()
pp(response.css('a::attr(href)').get())
pp(response.css('a::attr(href)').extract_first())
pp(response.css('a::attr(href)').getall())
pp(response.css('a::attr(href)').extract())
pp(response.css('a::attr(href)')[0].get())
pp(response.css('a::attr(href)')[0].extract())
pp(response.css('a::attr(href)')[0].getall())
print('--------------------------1.7 结束----------------------------')

# 2 Working with XPaths

# 2.1 Working with relative XPaths
divs = response.xpath('//div')
for a in divs.xpath('//a'):  # this is wrong - gets all <a> from the whole document
    print(a.get())
print('------------------------------------------------------')
for a in divs.xpath('.//a'):  # extracts all <a> inside
    print(a.get())
print('------------------------------------------------------')
for a in divs.xpath('a'):
    print(a.get())
print('---------------------------2.1 结束---------------------------')

# 2.2 When querying by class, consider using CSS
sel = Selector(text='<div class="hero shout"><time datetime="2014-07-23 19:00">Special date</time></div>')
pp(sel.css('.shout').xpath('./time/@datetime').getall())
print('---------------------------2.2 结束---------------------------')

# 2.3 Beware of the difference between //node[1] and (//node)[1]
sel = Selector(text="""
     <ul class="list">
         <li>1</li>
         <li>2</li>
         <li>3</li>
     </ul>
     <ul class="list">
         <li>4</li>
         <li>5</li>
         <li>6</li>
     </ul>""")
xp = lambda x: sel.xpath(x).getall()
pp(xp("//li[1]"))
pp(xp("(//li)[1]"))
pp(xp("//ul/li[1]"))
pp(xp("(//ul/li)[1]"))
print('---------------------------2.3 结束---------------------------')

# 2.4 Using text nodes in a condition
sel = Selector(text='<a href="#">Click here to go to the <strong>Next Page</strong></a>')
pp(sel.xpath('//a//text()').getall())  # take a peek at the node-set)
pp(sel.xpath("string(//a[1]//text())").getall())  # convert it to string)
pp(sel.xpath("//a[1]").getall())  # select the first node
pp(sel.xpath("string(//a[1])").getall())  # convert it to string)
pp(sel.xpath("//a[contains(.//text(), 'Next Page')]").getall())
pp(sel.xpath("//a[contains(., 'Next Page')]").getall())
print('---------------------------2.4 结束---------------------------')

# 2.5 Variables in XPath expressions
# `$val` used in the expression, a `val` argument needs to be passed
pp(response.xpath('//div[@id=$val]/a/text()', val='images').get())
pp(response.xpath('//div[count(a)=$cnt]/@id', cnt=5).get())
print('---------------------------2.5 结束---------------------------')

# 2.6 Removing namespaces
# scrapy shell https://feeds.feedburner.com/PythonInsider

# <?xml version="1.0" encoding="UTF-8"?>
# <?xml-stylesheet ...
# <feed xmlns="http://www.w3.org/2005/Atom"
#       xmlns:openSearch="http://a9.com/-/spec/opensearchrss/1.0/"
#       xmlns:blogger="http://schemas.google.com/blogger/2008"
#       xmlns:georss="http://www.georss.org/georss"
#       xmlns:gd="http://schemas.google.com/g/2005"
#       xmlns:thr="http://purl.org/syndication/thread/1.0"
#       xmlns:feedburner="http://rssnamespace.org/feedburner/ext/1.0">
#   ...

# >>> response.xpath("//link")
# []

# >>> response.selector.remove_namespaces()
# >>> response.xpath("//link")
# [<Selector xpath='//link' data='<link rel="alternate" type="text/html" h'>,
#     <Selector xpath='//link' data='<link rel="next" type="application/atom+'>,
#     ...

# 2.7 Using EXSLT extensions
# 2.7.1 Regular expressions
doc = """
<div>
    <ul>
        <li class="item-0"><a href="link1.html">first item</a></li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-inactive"><a href="link3.html">third item</a></li>
        <li class="item-1"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
</div>
"""
sel = Selector(text=doc, type="html")
pp(sel.xpath('//li//@href').getall())
pp(sel.xpath('//li[re:test(@class, "item-\d$")]//@href').getall())
print('---------------------------2.7.1 结束---------------------------')

# 2.7.2 Set operations
# doc = """
# <div itemscope itemtype="http://schema.org/Product">
#     <span itemprop="name">Kenmore White 17" Microwave</span>
#     <img src="kenmore-microwave-17in.jpg" alt='Kenmore 17" Microwave' />
#     <div itemprop="aggregateRating" itemscope itemtype="http://schema.org/AggregateRating">
#         Rated <span itemprop="ratingValue">3.5</span>/5
#         based on <span itemprop="reviewCount">11</span> customer reviews
#     </div>
#     <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
#         <span itemprop="price">$55.00</span>
#         <link itemprop="availability" href="http://schema.org/InStock" />In stock
#     </div>
#     Product description:
#     <span itemprop="description">0.7 cubic feet countertop microwave.
#     Has six preset cooking categories and convenience features like
#     Add-A-Minute and Child Lock.</span>
#     Customer reviews:
#     <div itemprop="review" itemscope itemtype="http://schema.org/Review">
#         <span itemprop="name">Not a happy camper</span> -
#         by <span itemprop="author">Ellie</span>,
#         <meta itemprop="datePublished" content="2011-04-01">April 1, 2011
#         <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
#         <meta itemprop="worstRating" content = "1">
#         <span itemprop="ratingValue">1</span>/
#         <span itemprop="bestRating">5</span>stars
#     </div>
#     <span itemprop="description">The lamp burned out and now I have to replace it. </span>
# </div>
# <div itemprop="review" itemscope itemtype="http://schema.org/Review">
#     <span itemprop="name">Value purchase</span> -
#     by <span itemprop="author">Lucas</span>,
#     <meta itemprop="datePublished" content="2011-03-25">March 25, 2011
#     <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
#         <meta itemprop="worstRating" content = "1"/>
#         <span itemprop="ratingValue">4</span>/
#         <span itemprop="bestRating">5</span>stars
#     </div>
#     <span itemprop="description">Great microwave for the price. It is small and
#     fits in my apartment.</span>
# </div>
# """
# sel = Selector(text=doc, type="html")
# for scope in sel.xpath('//div[@itemscope]'):
#     print("current scope:", scope.xpath('@itemtype').getall())
#     props = scope.xpath('''set:difference(./descendant::*/@itemprop, .//*[@itemscope]/*/@itemprop)''')
#     print(f"    properties: {props.getall()}")
#     print("")

# 2.7.3 Other XPath extensions
doc = """
<p class="foo bar-baz">First</p>
<p class="foo">Second</p>
<p class="bar">Third</p>
<p>Fourth</p>
"""
sel = Selector(text=doc, type="html")
pp(sel.xpath('//p[has-class("foo")]'))
pp(sel.xpath('//p[has-class("foo", "bar-baz")]'))
# 等同于以上代码
pp(sel.css('p.foo.bar-baz'))
pp(sel.xpath('//p[has-class("foo", "bar")]'))
