from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem


class OdishareporterSpider(CrawlSpider):
    name = 'odishareporter'
    start_urls = [f"https://odishareporter.in/post-sitemap{lot}.xml" for lot in range(1, 150)]

    # Rules for horizontal and vertical scrolling
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//table[@id='sitemap']/tbody/tr/td"), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=ScrapeprojectItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('header', "//h1[@class='single-post-title']//text()",
                    MapCompose(lambda text: text.strip()), Join())
        l.add_xpath('content', "//div[@class='entry-content clearfix single-post-content']/p//text()",
                    MapCompose(lambda text: text.strip()), Join())
        return l.load_item()
