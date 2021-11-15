from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem


class News18Spider(CrawlSpider):
    """
    Faced the following challenges:
        1. The URLs are without the hostnames
        2. There are intermediate elements in a div tag which contains the target text,
            that makes it parse unwanted texts.
    """
    name = 'news18'
    start_urls = ["https://odia.news18.com/odisha/"]

    # Rules for horizontal and vertical scrolling
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='older']/a"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='blog-list-blog']/p/a"), follow=True, callback='parse_item'),
    )

    def process_text(self, text):

        ...

    def parse_item(self, response):
        l = ItemLoader(item=ScrapeprojectItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('header', "//div[@id='article']//h1/text()",
                    MapCompose(lambda text: text.strip()), Join())
        l.add_xpath('content', "//div[@class='entry-content clearfix single-post-content']/p//text()",
                    MapCompose(lambda text: text.strip()), Join())
        return l.load_item()
