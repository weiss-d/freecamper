import scrapy


class QuotesSpider(scrapy.Spider):
    name = "test2"

    start_urls = ['https://bandcamp.com/artist_index/']

    def parse(self, response):
        artist_urls = response.css('.item>a::attr(href)').getall()
        for url in artist_urls:
            yield {url: url}

        next_page = response.css('.chosen').xpath("../following-sibling::li[1]/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
