import scrapy

NYP_STRING = "name your price"


class QuotesSpider(scrapy.Spider):
    name = "default_spider"

    start_urls = ["https://bandcamp.com/artist_index/"]

    def parse(self, response):
        artist_urls = response.css(".item>a::attr(href)").getall()
        yield from response.follow_all(artist_urls, self.parse_artist)

        next_page = (
            response.css(".chosen").xpath("../following-sibling::li[1]/a/@href").get()
        )
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_artist(self, response):
        print("Parsing artist:")
        if "releases" in response.url:
            print("Single album artist:")
            yield from self.parse_album(response)
        else:
            print("Parsing discography:")
            yield from response.follow_all(
                response.css(".music-grid-item>a::attr(href)").getall(),
                self.parse_album,
            )

    def parse_album(self, response):
        print("Parsing Album:")
        if response.css(".buyItemNyp::text").get() == NYP_STRING:
            print("FREE Album!", response.css(".buyItemNyp::text").get())
            yield {
                "artist": response.xpath('//span[@itemprop="byArtist"]/a/text()').get(),
                "album": response.css(".trackTitle::text").get().strip(),
                "year": response.xpath(
                    '//meta[@itemprop="datePublished"]/@content'
                ).get()[:4],
                "tags": response.css(".tag::text").getall(),
                "url": response.url,
            }
