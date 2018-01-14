import scrapy
import json
from mic.spiders import *


class MicSitemapSpider(scrapy.Spider):
    name = "mic_sitemap"
    __links_filename = 'sitemap-article-links'

    def start_requests(self):
        urls = [
            '{}/sitemap.xml'.format(get_domain_name())
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        xpath = '//*[local-name() = "url"]/*[local-name() = "loc" ' \
                'and starts-with(text(), "{0}/articles/") ' \
                'and not(starts-with(text(), "{0}/articles/tags/")) ' \
                'and not(starts-with(text(), "{0}/articles/author/"))]/text()'.format(get_domain_name())
        article_links = [link for link in response.xpath(xpath).extract()]
        for article_link in article_links:
            yield response.follow(article_link, self.parse_article)
        filename = '{}/{}'.format(get_output_dir(), self.__links_filename)
        with open(filename, 'wb') as f:
            f.write(json.dumps(article_links))
        self.log('Saved file %s' % filename)

    def parse_article(self, response):
        filename = parse_article(response)
        self.log('Saved file %s' % filename)
