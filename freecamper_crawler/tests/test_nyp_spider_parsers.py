from pathlib import Path

import pytest
from scrapy.http import TextResponse, Request

from freecamper_crawler.spiders import nyp_spider

@pytest.fixture
def fake_response():
    def _response(url: str, html_file: Path) -> TextResponse:
        request = Request(url)

        import os
        print(os.getcwd())

        with open(html_file, "r") as sample:
            return TextResponse(url=url,
                            request=request,
                            body=sample.read().encode(),
                            )
    return _response

def test_parse_single_track_album(fake_response):
    response = fake_response("http://test.url", Path("freecamper_crawler/tests/page_samples/album/1_track_album.html"))
    result = {"artist": "Orphic",
              "album": "Orphic 4",
              "year": "2020",
              "tracks": 1,
              "tags": ['jazz', 'acoustic',  'contemporary', 'Bristol'],
              "url": "http://test.url"}

    spider = nyp_spider.nypSpider()

    assert next(spider.parse_album(response)) == result
