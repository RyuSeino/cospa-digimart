# -*- coding: utf-8 -*-
import scrapy

from digimart_new_items import items


class DigimartSpider(scrapy.Spider):
    name = 'digimart'
    allowed_domains = ['digimart.net']

    start_urls = [
        'https://www.digimart.net/search?dispMode=ALL&shopNo=&keywordOr=&keywordPhrase=&productName=&nosalep=false&noshopsalep=false&officialCouponShopP=false&categoryId=&categoryNames=&category12Id=101&category3Id=&brandnames=&brandnames=&brandnames=&keywordAnd=&areaId=&priceFrom=&priceTo=&productTypes=NEW_SALE&productTypes=SALE&nosoldoutp=on&x=16&y=11&manufactureYearFrom=&manufactureYearTo=&weightOptionFrom=&weightOptionTo=&term=&stringsoption=&pickupOption=&pickupComponentOption=&otherOption=&fretOption=&neckScaleOption=&bodyOption=&tremolantOption=&fingerboardOption=&neckjointOption=&neckOption=&topMaterialOption=&sideMaterialOption=&backMaterialOption=&bodysizeOption=&bodyShapeOption=&materialOption=&keywordNot=']



    def parse(self, response):

        for sel in response.css('div.itemSearchBlock'):
            item = items.DigimartNewItemsItem()
            item['name'] = sel.css('div.itemSearchBox > p.ttl > a::text').extract_first()
            item['price'] = sel.css('p.price::text').extract_first()
            yield item

        sel = response.css('ul.pagerList').xpath("//a[contains(.//text(), '次')]/@href").extract_first()
        url = response.urljoin(sel)
        yield scrapy.Request(url, callback=self.parse)



