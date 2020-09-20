# 🎵 freecamper

Crawler and database for enhancing discovery experience on Bandcamp.com
***

[Bandcamp](https://bandcamp.com/) is a fascinating platform, where everyone can publish their music in high-quality format, without censorship or copyright issues. You can set arbitrary price for your art and all money except of 15% will go directly to you, while a buyer gets FLAC download and unlimited on-line streaming. There is also an option to set 'zero or more' price called 'name your price' or NYP. It is commonly used for albums released under Creative Commons license.

Unfortunately, the discovery system of Bandcamp is not that perfect. Let say you cannot get all releases with a certain tag for a specific year, or separate singles from LPs & EPs. Also there's no straight way to search for free/NYP releases.

So the goal of this project is to make a crawler that will scrape all possible information (i.e. tags, release date and number of tracks etc.) from every album on Bandcamp (that's a lot!) neatly and slowly not to put excessive load on their servers. Put this info in a database and make a public UI to it, until maybe BC will upgrade its discovery options.

## What is done

I implemented a Scrapy spider, that can find all free/NYP releases on the platform and provide the following data:

* Artist / Album

* Release date

* Tags

* Release URL

The data is saved in a CSV file.

To run it you'll need `Pyton >=3.7` and `scrapy` installed.
Clone the repository, `cd` to `freecamp_crawler` folder.
Run this command:
```bash
$ scrapy crawl nyp_spider
```
Processing speed is now set to about 2500 albums per hour.
Results would be saved in `nyp_spider` folder in a CSV file.
To stop it press `Ctrl+C` once and wait untill spider termitanes. 

## What is to be done

- [ ] Make a crawler to analyze all (1500000+) releases on BC and extract also the number of tracks and cover thumbnails.
- [ ] Put all these in a database which will be updated by the crawler daily.
- [ ] Make a simple webapp to access the data.

## What is not to be done

❌ Any automatic audio downloaders, rippers etc.

## How to participate
Feel free to open an issue or make a PR. No rules yet. 🙂