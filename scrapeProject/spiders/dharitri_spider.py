import scrapy


class ArticleLinksSpider(scrapy.Spider):
    name = "article_links"
    start_urls = [f"https://www.dharitri.com/{year}/{month:02}" for year in range(2020, 2022) for month in range(1, 13)]

    def parse(self, response):
        for article in response.css("div.caption"):
            yield {
                "article_link": article.css("a.text-black").attrib['href'],
            }
        yield from response.follow_all(css="a.page.larger", callback=self.parse)
