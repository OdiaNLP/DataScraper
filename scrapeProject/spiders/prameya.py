from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem


class PrameyaSpider(CrawlSpider):
    name = 'prameya'
    start_urls = ["http://www.prameya.com/"]

    # Rules for horizontal and vertical scrolling
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='next page-numbers']"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='read-title']/h4/a"), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=ScrapeprojectItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('header', "//h1[@class='entry-title']//text()",
                    MapCompose(lambda text: text.strip()), Join())
        l.add_xpath('content', "//div[@class='entry-content read-details color-tp-pad no-color-pad']/p//text()",
                    MapCompose(lambda text: text.strip()), Join())
        return l.load_item()
