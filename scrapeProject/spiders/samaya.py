from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem


class SamayaSpider(CrawlSpider):
    name = 'samaya'
    start_urls = [
        "https://www.samayalive.in/category/business/",
        "https://www.samayalive.in/category/entertainment/",
        "https://www.samayalive.in/category/politics/",
        "https://www.samayalive.in/category/sports/",
        "https://www.samayalive.in/category/world/",
        "https://www.samayalive.in/category/video/",
        "https://www.samayalive.in/category/health/",
        "https://www.samayalive.in/category/interview/",
        "https://www.samayalive.in/category/literature/",
        "https://www.samayalive.in/category/lifestyle/",
        "https://www.samayalive.in/category/nation/",
        "https://www.samayalive.in/category/district/",
        "https://www.samayalive.in/category/astrology/",
        "https://www.samayalive.in/category/crime/",
        "https://www.samayalive.in/category/odisha/",
        "https://www.samayalive.in/category/poem/",
        "https://www.samayalive.in/category/feature/",
        "https://www.samayalive.in/category/fitness/",
        "https://www.samayalive.in/category/agriculture/",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='next page-numbers']"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='post-title post-url']"), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=ScrapeprojectItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('header', "//h1[@class='single-post-title']//text()",
                    MapCompose(lambda text: text.strip()), Join())
        l.add_xpath('content', "//div[@class='entry-content clearfix single-post-content']//text()",
                    MapCompose(lambda text: text.strip()), Join())
        return l.load_item()
