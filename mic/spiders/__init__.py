# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os

__output_dir = 'Output'
__articles_dir = '{}/articles'.format(__output_dir)
__domain_name_file = 'domain-name.txt'


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


def parse_article(response):
    filename = '{0}/{1}'.format(get_articles_dir(), text_to_filename(response.url.rsplit('/', 1)[-1]))
    with open(filename, 'wb') as f:
        f.write(response.css('div.sp-article-column').extract_first().encode('utf-8'))
    return filename


def text_to_filename(text):
    valid_chars='-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(c for c in text if c in valid_chars)


def get_domain_name():
    with open(__domain_name_file, 'r') as f:
        return f.readline()