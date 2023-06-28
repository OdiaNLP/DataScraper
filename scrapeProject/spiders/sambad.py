from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem
from datetime import date, timedelta


def fetch_start_urls():
    start_date = date(2021, 11, 16)
    end_date = date.today()
    delta = timedelta(days=1)
    urls = []
    while start_date <= end_date:
        urls += [f"https://sambad.in/date/{start_date.strftime('%Y/%m/%d')}"]
        start_date += delta
    return urls


class SambadSpider(CrawlSpider):
    name = 'sambad'
    start_urls = fetch_start_urls()

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='btn-bs-pagination next']"), follow=True),
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
