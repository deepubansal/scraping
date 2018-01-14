import scrapy
import json
from mic.spiders import *


class MicLicSpider(scrapy.Spider):
    name = "mic_lic"
    __links_filename = 'lic-links'

    def start_requests(self):
        urls = [
            '{0}/articles/tags/lic'.format(get_domain_name())
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        article_links = []
        for article in response.css('article.article-content'):
            article_link = {
                'link': article.css('a.title-link::attr("href")').extract_first(),
                'title': article.css('div.title::text').extract_first(),
            }
            article_links.append(article_link)
            next_page = article.css('a.title-link::attr("href")').extract_first()
            if next_page is not None:
                yield response.follow(next_page, self.parse_article)
        filename = '{}/{}'.format(get_output_dir(), self.__links_filename)
        with open(filename, 'wb') as f:
            f.write(json.dumps(article_links))
        self.log('Saved file %s' % filename)

    def parse_article(self, response):
        filename = parse_article(response)
        self.log('Saved file %s' % filename)
