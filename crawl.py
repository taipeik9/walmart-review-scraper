import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import multiprocessing

import re

from walmart.spiders.products import ProductsSpider
from walmart.spiders.reviews import ReviewSpider

def run_crawler(spider):
    process = CrawlerProcess(settings=spider['settings'])
    process.crawl(spider['spider'], **spider['arguments'])
    process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
    url = 'https://www.walmart.ca/browse/beauty/skin-care/6000198722778-6000195305341?f=40601&icid=browse_l2_beauty_best_sellers_3754_HJ22HN793B&fromFC=true'
    
    arguments = dict(
        url = url,
        id = re.findall(r'-[0-9]+', url)[-1][1:],
        query = re.search(r'\w+=.+', url).group(),
        limit = 30
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
        'arguments' : {'url' : url}
    })

    for spider in spiders:
        p = multiprocessing.Process(target=run_crawler, args=(spider,))
        p.start()
        p.join()