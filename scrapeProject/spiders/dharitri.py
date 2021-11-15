from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem


class DharitriSpider(CrawlSpider):
    name = 'dharitri'
    start_urls = [f"https://www.dharitri.com/{year}/{month:02}" for year in range(2020, 2022) for month in range(1, 13)]

    # Rules for horizontal and vertical scrolling
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='nextpostslink']"), follow=True),
        Rule(LinkExtractor(restrict_css="a.text-black"), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=ScrapeprojectItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('header', "//header[@class='cono']//h1/text()",
                    MapCompose(lambda text: text.strip()), Join())
        l.add_xpath('content', "//div[@class='p-t-20']/p//text()",
                    MapCompose(lambda text: text.strip()), Join())
        return l.load_item()
