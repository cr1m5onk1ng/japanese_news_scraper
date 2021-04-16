import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

class LivedoorSpider(scrapy.Spider):
    name = "livedoor_articles"
    start_urls = ["https://news.livedoor.com/"]

    def parse(self, response):
        cats = response.css('#globalNav a')[2:-5]
        for cat_link in cats:
            link = response.urljoin(cat_link.attrib['href'])[:-1]
            category = link.split("/")[-1]
            print(f"CURRENT CATEGORY: {category}")
            yield Request(url=link, callback=self.collect_articles, cb_kwargs=dict(category=category))

    def collect_articles(self, response, category):
        articles_links = response.css('#main a')
        for link, title in zip(articles_links, titles):
            l = response.urljoin(link.attrib['href']).replace('/topic/', '/article/')
            yield Request(url=l, callback=self.parse_article, cb_kwargs=dict(category=category))
        next_page_links = response.css('.pager a')
        yield from response.follow_all(next_page_links, callback=self.collect_articles)

    def parse_article(self, response, category):
        title = response.css('.articleTtl::text').get()
        paragraphs = response.css('.articleBody p::text').getall()
        text = '\n'.join(paragraphs)
        yield {
            "title": title,
            "category": category,
            "text": paragraphs
        }

