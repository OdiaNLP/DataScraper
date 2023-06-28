from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule

from scrapeProject.items import ScrapeprojectItem
from datetime import date, timedelta


def fetch_start_urls():
    # start date: https://www.samajalive.in/date/2018/02/05
    start_date = date(2021, 12, 27)
    end_date = date.today()
    delta = timedelta(days=1)
    urls = []
    while start_date <= end_date:
        urls += [f"https://www.samajalive.in/date/{start_date.strftime('%Y/%m/%d')}"]
        start_date += delta
    return urls


class SamajaSpider(CrawlSpider):
    name = 'samaja'
    start_urls = fetch_start_urls()

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='older']/a"), follow=True),
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
