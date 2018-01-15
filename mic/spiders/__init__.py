# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os
import json

__output_dir = 'Output'
__articles_dir = '{}/articles'.format(__output_dir)
__domain_name_file = 'domain-name.txt'
__article_info_file = '{}/articles.info'.format(__output_dir)


def get_output_dir():
    return ensure_dir(__output_dir)


def get_articles_dir():
    return ensure_dir(__articles_dir)


def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    return path


def ensure_json_file(path):
    if not os.path.isfile(path):
        if os.path.isdir(path):
            raise
        with open(path, 'w') as f:
            f.write('[]')


def parse_article(response):
    slug = response.url.rsplit('/', 1)[-1]
    filename = text_to_filename(slug)
    file_path = '{0}/{1}'.format(get_articles_dir(), filename)
    with open(file_path, 'wb') as f:
        f.write(response.css('div.sp-article-column').extract_first().encode('utf-8'))
    article_info = {'article': filename, 'information':
        {'slug': slug, 'title': response.css('div.sp-header-txt::text').extract_first().strip(),
         'title-img': response.css('div.entry-thumb img::attr("src")').extract_first()}}
    save_article_info(article_info)
    return file_path


def save_article_info(article_info):
    ensure_json_file(__article_info_file)
    with open(__article_info_file) as f:
        data = json.loads(f.read())
    data.append(article_info)
    with open(__article_info_file, 'wb') as f:
        f.write(json.dumps(data))


def text_to_filename(text):
    valid_chars='-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(c for c in text if c in valid_chars)


def get_domain_name():
    with open(__domain_name_file, 'r') as f:
        return f.readline()