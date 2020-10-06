from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class nypSpider(CrawlSpider):
    name = "nyp_spider"

    start_urls = ["https://bandcamp.com/artist_index/"]

    # INDEX_PAGE_LIMIT = 2
    rules = (
        # Exctract links to artist profiles from Artist Index page
        Rule(
            LinkExtractor(
                restrict_css=[".item"],
            ),
            callback="parse_artist",
        ),
        # Extract link to the next Index page
        Rule(
            LinkExtractor(
                restrict_xpaths=[
                    "//span[contains(concat(' ', normalize-space(@class), ' '), ' chosen ')]/parent::li/following-sibling::li[1]"
                ],
                # allow=(rf".*{INDEX_PAGE_LIMIT}\Z",) # limiter of Artist Index pages for testing purposes
            )
        ),
    )

    total_artists_crawled = 0
    total_albums_crawled = 0

    def parse_artist(self, response):
        """Parses an artist page.
        This page may represent one album, discography or nothing.
        See # comments below."""

        self.logger.info("== == Crawling artis: %s", self.total_artists_crawled + 1)

        url = response.url.split("/")
        if url[-1] == "releases":  # Artist has only one album
            self.total_artists_crawled += 1
            yield self.parse_album(response)
        elif url[-1] == "music":  # Artist has discography on the firs page
            self.total_artists_crawled += 1
            yield from self.parse_discography(response)
        else:  # Artist has no albums or has a discography, but first page represents one album
            yield response.follow("music", callback=self.parse_artist)

    def parse_discography(self, response):
        """Just extracting album links from tiled discog and sending them
        to parse_album()"""

        album_links = response.css(".music-grid-item>a")
        yield from response.follow_all(
            album_links,
            self.parse_album,
        )

    def parse_album(self, response):
        """Final point, where an album is checked for free option,
        and id it's available, all necessary data is extracted."""

        self.total_albums_crawled += 1
        self.logger.info(
            "== == == Crawling album. Overall number: %s", self.total_albums_crawled
        )

        if response.css(".buyItemNyp::text").get() == "name your price":
            # Artist
            artist = response.xpath('//span[@itemprop="byArtist"]/a/text()').get()
            # Album
            album = response.css(".trackTitle::text").get().strip()
            # Release Year
            try:
                year = int(
                    response.css(".tralbum-credits::text").get().strip(" \n")[-4:]
                )
            except ValueError:
                year = ""
            # Number of tracks
            tracks = response.css(
                ".track_row_view:last-child>.track-number-col>div::text"
            ).get()
            # Tags
            tags = response.css(".tag::text").getall()
            # License
            if license_text := "".join(
                response.css("#license.info.license::text").getall()
            ).strip(" \n"):
                license_url = ""
            else:
                license_object = response.css("#license.info.license>a:last-child")
                license_text = license_object.css("a::text").get()
                license_url = license_object.css("a::attr(href)").get()

            return {
                "artist": artist,
                "album": album,
                "year": year,
                "tracks": int(tracks[:-1]) if tracks else 1,
                "tags": tags,
                "license": {"text": license_text, "url": license_url},
                "url": response.url,
            }
