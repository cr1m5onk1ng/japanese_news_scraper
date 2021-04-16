import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from selenium import webdriver
import time
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"

class MainichiSpider(scrapy.Spider):
    name = "mainichi_articles"
    start_urls = ["https://mainichi.jp/"]

    def parse(self, response):
        CATEGORIES = {
            "shakai": ("16178663690", "55"), 
            "seiji": ("16178693049", "90"), 
            "biz": ("16178694068", "17"),
            "world": ("16178695273", "90"),
            "sports": ("16178695889", "32"),
            "science": ("16178696798", "47"),
            "culture": ("16178697480", "26"),
            "life": ("16178698136", "49"),
            "opinion": ("16178699249", "72")
        }
        for cat, params in CATEGORIES.items(): #avoid first category
            link = response.urljoin(cat)
            yield Request(url=link, callback=self.collect_articles, cb_kwargs=dict(category=cat, params=params))

    def collect_articles(self, response, category, params):
        req_id, start_page = params
        start_page = int(start_page)
        for i in range(3, 23):
            if i == 3:
                new_page = f"{i}?&_={req_id}{start_page}"
            else:
                new_page = f"{i}?&&_={req_id}{start_page}"
            start_page+=1
            url = response.urljoin(new_page)
            yield Request(
                url,
                method="GET",
                callback=self.parse_response,
                cb_kwargs=dict(category=category)
            )
        """
        #titles = response.css('#article-list .articlelist-title::text').getall()
        articles_links = response.css('#article-list a')
        for link in articles_links:
            l = response.urljoin(link.attrib['href'])
            yield Request(url=l, callback=self.parse_article, cb_kwargs=dict(category=category))
        next_url = response.css('#nexturl').attrib['data-searchnexturl']
        if next_url is not None:
            response.follow(next_url, callback=self.collect_articles)
        """

    def parse_response(self, response, category):
        script_json = response.css("script[type='application/ld+json']::text").get()
        try:
            parsed_json = json.loads(script_json)
        except:
            parsed_json = {}
        #print(f"PARSED JSON: {parsed_json}")
        if parsed_json:
            articles_list = parsed_json["hasPart"]
            if articles_list is not None:
                for art in articles_list:
                    url = art["url"]
                    assert url is not None
                    yield Request(
                        url, 
                        callback=self.parse_article, 
                        cb_kwargs=dict(category=category)
                    )

    def parse_article(self, response, category):
        title = response.css('.title-page::text').get()
        paragraphs = response.css('#articledetail-body p::text').getall()
        text = '\n'.join(paragraphs)
        yield {
            "url": response.url,
            "title": title,
            "category": category,
            "text": text
        }



