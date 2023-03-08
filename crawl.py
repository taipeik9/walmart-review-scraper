from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import multiprocessing

import re

import sys

from walmart.spiders.products import ProductsSpider
from walmart.spiders.reviews import ReviewSpider

def run_crawler(spider):
    process = CrawlerProcess(settings=spider['settings'])
    process.crawl(spider['spider'], **spider['arguments'])
    process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
    url = sys.argv[1]
    try:
        limit = int(sys.argv[2])
    except IndexError:
        limit = None
    
    type = re.search(r'walmart.ca\/\w+', url).group().replace('walmart.ca/', '')

    if type == 'brand':
        type = 'browse'
        query = f'f={re.search(r"[0-9]+", url).group()}'
    else:
        query = re.search(r'\w+=.+', url).group()

    if re.search(r'-[0-9]+', url):
        id = f"&c={re.findall(r'-[0-9]+', url)[-1][1:]}"
    else:
        id = ''
    
    if (not re.search(r'c=[0-9]+', query)) and (type == 'search'):
        query = f'{query}&c=all'
        

    arguments = dict(
        url = url,
        id = id,
        query = query,
        limit = limit,
        type = type
    )

    spiders = []

    # Getting products spider settings
    products_settings = get_project_settings()
    products_settings['FEED_FORMAT'] = 'json'
    products_settings['FEED_URI'] = 'products.json'

    spiders.append({
        'settings' : products_settings,
        'spider' : ProductsSpider,
        'arguments' : arguments
    })

    # Getting reviews spider settings
    reviews_settings = get_project_settings()
    reviews_settings['FEED_FORMAT'] = 'csv'
    reviews_settings['FEED_URI'] = 'reviews.csv'

    spiders.append({
        'settings' : reviews_settings,
        'spider' : ReviewSpider,
        'arguments' : {}
    })

    for spider in spiders:
        p = multiprocessing.Process(target=run_crawler, args=(spider,))
        p.start()
        p.join()