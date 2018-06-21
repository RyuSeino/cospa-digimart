# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse, urljoin
from digimart_new_items import items


class DigimartSpider(CrawlSpider):
    name = 'digimart'
    allowed_domains = ['digimart.net']

    start_urls = [
        'https://www.digimart.net/search?dispMode=ALL&nosalep=false&category12Id=101&category3Id=&productTypes=NEW_SALE&productTypes=SALE&nosoldoutp=on']

    rules = [
        Rule(LinkExtractor(r'/search\?.*NEW_SALE'), callback='parse_item', follow=True)
    ]


    def parse_item(self, response):

        for sel in response.css('div.itemSearchBlock'):

            base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(response.url))

            price = sel.css('p.price::text').extract_first().replace('¥', '')
            price = price.replace(',', '')
            if int(price) < 150000:
                item = items.DigimartNewItemsItem()
                item['url'] = urljoin(base_url, sel.css('div.itemSearchBox > p.ttl > a::attr(href)').extract_first())
                item['name'] = sel.css('div.itemSearchBox > p.ttl > a::text').extract_first()
                item['price'] = sel.css('p.price::text').extract_first()

                yield item

