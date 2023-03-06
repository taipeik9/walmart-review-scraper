import scrapy

import json


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.walmart.ca"]

    headers={
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.walmart.ca/browse/beauty/skin-care/facial-cleansers-toners/face-wash/6000198722778-6000195305341-6000195308541-6000198737951?icid=browse_l2_beauty_face_wash_3744_3QFXRBEJOA&fromFC=true',
        'origin': 'https://www.walmart.ca'
    }

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.walmart.ca/api/bsp/browse?lang=en&c=6000195309547&p=1',
            headers=self.headers
        )

    def parse(self, response):
        r = json.loads(response.body)

        try:
            products = r['items']['products']
            category = r['seoMetadata']['nodeName']
        except KeyError:
            products = r['products']
            category = response.request.meta['category']

        for id in products:
            yield {
                'product_id' : products[id]['id'],
                'sku_ids' : products[id]['skuIds'],
                'name' : products[id]['name'],
                'brand' : products[id]['skus'][products[id]['skuIds'][0]]['brand'].get('name'),
                'avg_rating' : products[id]['rating']['averageRating'],
                'total_ratings' : products[id]['rating']['totalCount'],
                'category' : category,
                'desc' : products[id]['description'],
                'facets' : products[id]['skus'][products[id]['skuIds'][0]]['facets']
            }

        if r.get('items'):
            payload = {
                'products': r['items']['productsToFetch'],
                'lang' : 'en'
            }

            yield scrapy.Request(
                url='https://www.walmart.ca/api/bsp/fetch-products?experience=whiteGM',
                headers=self.headers,
                method='POST',
                body=json.dumps(payload),
                meta={
                    'category' : category
                }
            )
        
