from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem


class PragativadiSpider(CrawlSpider):
    name = 'pragativadi'
    start_urls = ["https://pragativadinews.com/blog/"]

    # Rules for horizontal and vertical scrolling
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='older']/a"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//h2/a[@class='post-url post-title']"), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=ScrapeprojectItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('header', "//h1[@class='single-post-title']//text()",
                    MapCompose(lambda text: text.strip()), Join())
        l.add_xpath('content', "//div[@class='entry-content clearfix single-post-content']/p//text()",
                    MapCompose(lambda text: text.strip()), Join())
        return l.load_item()
