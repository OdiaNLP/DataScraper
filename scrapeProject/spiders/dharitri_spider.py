import datetime
import socket

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

from scrapeProject.items import ScrapeprojectItem


class ArticleLinksSpider(scrapy.Spider):
    name = "article_links"
    start_urls = [f"https://www.dharitri.com/{year}/{month:02}" for year in range(2020, 2022) for month in range(1, 13)]

    def parse(self, response):
        for article in response.css("div.caption"):
            yield from article.follow_all(css="a.text-black", callback=self.parse_articles)
        yield from response.follow_all(css="a.page.larger", callback=self.parse)

    def parse_articles(self, response):
        # header = response.xpath("//header[@class='cono']//h1/text()").extract()
        # [text.strip() for text in header if text.strip()]
        # article_text: List[str] = response.xpath("//div[@class='p-t-20']/p//text()").extract()
        l = ItemLoader(item=ScrapeprojectItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('header', "//header[@class='cono']//h1/text()",
                    MapCompose(unicode.strip))
        l.add_xpath('content', "//div[@class='p-t-20']/p//text()",
                    MapCompose(unicode.strip))

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
