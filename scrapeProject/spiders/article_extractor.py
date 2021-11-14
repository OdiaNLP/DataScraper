import json_lines
import scrapy


def get_urls():
    with open("../articles.jl", encoding="utf-8", mode="rb") as articles:
        for article in json_lines.reader(articles):
            yield article["article_link"]


class ArticlesContentSpider(scrapy.Spider):
    name = "articles"
    start_urls = get_urls()

    def parse(self, response):
        # header = response.xpath("//header[@class='cono']//h1/text()").extract()
        # [text.strip() for text in header if text.strip()]
        # article_text: List[str] = response.xpath("//div[@class='p-t-20']/p//text()").extract()
        for article in response.css("h1.my_menu"):
            yield {
                "article_link": article.css("a.text-black").attrib['href'],
            }
