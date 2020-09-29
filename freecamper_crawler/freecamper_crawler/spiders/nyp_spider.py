from datetime import datetime

import scrapy


NYP_STRING = "name your price"


class nypSpider(scrapy.Spider):
    name = "nyp_spider"

    start_urls = ["https://bandcamp.com/artist_index/"]

    def parse(self, response):
        """Parses Bandcamp artist index.
        This index by default is sorted by time (newest first)."""

        artist_urls = response.css(".item>a::attr(href)").getall()
        yield from response.follow_all(artist_urls, self.parse_artist)

        next_page = (
            response.css(".chosen").xpath("../following-sibling::li[1]/a/@href").get()
        )
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_artist(self, response):
        """Parses an artist page.
        If the artist has only one release, the artist's page represents this release.
        Whole page is passed to parse_album().
        If the artist has multiple releases, this page is in form of discography list.
        Links to albums are then extracted and passed to parse_album()."""

        if "releases" in response.url:
            yield from self.parse_album(response)
        elif "music" in response.url:
            yield from response.follow_all(
                response.css(".music-grid-item>a::attr(href)").getall(),
                self.parse_album,
            )
        else:
            yield response.follow("music", callback=self.parse_artist)


    def parse_album(self, response):
        """Parses an album.
        Data is only extracted if the album allows free FLAC download."""

        if response.css(".buyItemNyp::text").get() == NYP_STRING:
            artist = response.xpath('//span[@itemprop="byArtist"]/a/text()').get()
            album = response.css(".trackTitle::text").get().strip()

            try:
                release_date = datetime.strptime(
                    response.xpath('//meta[@itemprop="datePublished"]/@content').get(),
                    "%Y%m%d",
                )
            except TypeError:
                release_date = None

            tracks = response.css(
                ".track_row_view:last-child>.track-number-col>div::text"
            ).get()

            tags = response.css(".tag::text").getall()

            yield {
                "artist": artist,
                "album": album,
                "year": release_date.year if release_date else "",
                "tracks": int(tracks[:-1]) if tracks else 1,
                "tags": tags,
                "url": response.url,
            }
