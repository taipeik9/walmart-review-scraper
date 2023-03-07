import scrapy
from scrapy.exceptions import CloseSpider

import json


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.walmart.ca"]
    total_products = 0

    custom_settings = {
        'HTTPERROR_ALLOWED_CODES' : [403]
    }

    headers={
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.walmart.ca',
        # 'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    def __init__(self, url, id, query, limit, *args, **kwargs):
        super(ProductsSpider, self).__init__(*args, **kwargs)
        self.id = id
        self.query = query
        self.limit = limit
        self.headers['referer'] = url
        
    
    def start_requests(self):
        yield scrapy.Request(
            url=f'https://www.walmart.ca/api/bsp/browse?lang=en&c={self.id}&experience=whiteGM&{self.query}&p=1',
            headers=self.headers,
            meta={
                'page' : 2
            }
        )
        

    def parse(self, response):
        r = json.loads(response.body)
        products = r['items']['products']

        for id in products:
            yield dict(
                product_id = products[id]['id'],
                sku_ids = products[id]['skuIds'],
                name = products[id]['name'],
                brand = products[id]['skus'][products[id]['skuIds'][0]]['brand'].get('name'),
                avg_rating = products[id]['rating']['averageRating'] if products[id]['rating'] else None,
                total_ratings = products[id]['rating']['totalCount'] if products[id]['rating'] else None,
                desc = products[id]['description'],
                facets = products[id]['skus'][products[id]['skuIds'][0]]['facets']
            )
            if self.limit:
                self.total_products += 1
                if self.total_products >= self.limit:
                    raise CloseSpider("Limit Reached")

        if r['items']['productsToFetch']:
            payload = {
                'products': r['items']['productsToFetch'],
                'lang' : 'en'
            }
            yield scrapy.Request(
                url='https://www.walmart.ca/api/bsp/fetch-products?experience=whiteGM',
                headers=self.headers,
                method='POST',
                body=json.dumps(payload),
                callback=self.parse_fetch
            )

        if r['items']['products']:
            yield scrapy.Request(
                url=f'https://www.walmart.ca/api/bsp/browse?lang=en&c={self.id}&experience='
                f'whiteGM&{self.query}&p={response.request.meta["page"]}',
                headers=self.headers,
                meta={
                    'page' : response.request.meta['page'] + 1
                }
            )
        

    def parse_fetch(self, response):
        r = json.loads(response.body)
        products = r['products']

        for id in products:
            yield dict(
                product_id = products[id]['id'],
                sku_ids = products[id]['skuIds'],
                name = products[id]['name'],
                brand = products[id]['skus'][products[id]['skuIds'][0]]['brand'].get('name'),
                avg_rating = products[id]['rating']['averageRating'] if products[id]['rating'] else None,
                total_ratings = products[id]['rating']['totalCount'] if products[id]['rating'] else None,
                desc = products[id]['description'],
                facets = products[id]['skus'][products[id]['skuIds'][0]]['facets']
            )
            if self.limit:
                self.total_products += 1
                if self.total_products >= self.limit:
                    raise CloseSpider("Limit Reached")

            