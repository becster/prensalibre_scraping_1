# -*- coding: utf-8 -*-
import scrapy
from prensalibre_daily.items import articles, article

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['prensalibre.com']
    start_urls = ['https://prensalibre.com/']

    def parse(self, response):
        host = self.allowed_domains[0]

        for link in response.css(".story-title > a"):
            link = f"{link.attrib.get('href')}"
            title = link
            yield response.follow(link,callback=self.parse_detail, meta={'URL' : link,'title':title})

    def parse_detail(self,response):
        items = articles()
        item = article()

        items["link"] = response.meta["link"]
        item["title"] = response.meta["title"]
        item["paragraph"] = list()

        for text in response.css(".sart-content > p::text").extract():
            item["paragraph"].append(text)
        
        items["body"] = item
        return items
