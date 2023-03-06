import scrapy

import json
import time
import logging


class ReviewSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["api.bazaarvoice.com"]

    headers={
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.walmart.ca/browse/beauty/skin-care/facial-cleansers-toners/face-wash/6000198722778-6000195305341-6000195308541-6000198737951?icid=browse_l2_beauty_face_wash_3744_3QFXRBEJOA&fromFC=true',
        'origin': 'https://www.walmart.ca'
    }

    def start_requests(self):
        with open('products.json') as f:
            products = json.load(f)
        
        for product in products:
            yield scrapy.Request(
                url='https://api.bazaarvoice.com/data/reviews.json?resource=reviews&filtered'
                'stats=reviews&Stats=Reviews&passkey=e6wzzmz844l2kk3v6v7igfl6i&apiversion=5.5&'
                f'displaycode=2036-en_ca&action=REVIEWS_N_STATS&filter=productid%3Aeq%3A{product["product_id"]}&'
                'filter=isratingsonly%3Aeq%3Afalse&filter_reviews=contentlocale%3Aeq%3Aen_CA%2Cen_GB%2Cen_'
                'US%2Cen_CA&include=authors%2Cproducts&limit=100&offset=0&sort=submissiontime%3Adesc',
                headers=self.headers,
                meta={
                    'id' : product['product_id'],
                    'offset' : 100,
                    'retry_count' : 0
                }
            )

    def parse(self, response):
        r = json.loads(response.body)

        # retrying on blank results
        if not r['Results'] and (response.request.meta['offset'] - 100 <= r['TotalResults']):
            retry = response.request.copy()
            if retry.meta['retry_count'] < 5:
                retry.meta['retry_count'] += 1
                logging.warning(f'Retrying Request: {retry.url}')
                time.sleep(3)
                yield retry
        elif response.request.meta['offset'] - 100 <= r['TotalResults']:
            for result in r['Results']:
                yield {
                    'product_id' : result['ProductId'],
                    'review_id' : result['Id'],
                    'title' : result['Title'],
                    'rating' : result['Rating'],
                    'text' : result['ReviewText'],
                    'date' : result['SubmissionTime'],
                    'pos_feedback_count' : result['TotalPositiveFeedbackCount'],
                    'client_res_count' : result['TotalClientResponseCount']
                }
            
            yield scrapy.Request(
                url='https://api.bazaarvoice.com/data/reviews.json?resource=reviews&filtered'
                'stats=reviews&Stats=Reviews&passkey=e6wzzmz844l2kk3v6v7igfl6i&apiversion=5.5&'
                f'displaycode=2036-en_ca&action=REVIEWS_N_STATS&filter=productid%3Aeq%3A{response.request.meta["id"]}&'
                'filter=isratingsonly%3Aeq%3Afalse&filter_reviews=contentlocale%3Aeq%3Aen_CA%2Cen_GB%2Cen_'
                f'US%2Cen_CA&include=authors%2Cproducts&limit=100&offset={response.request.meta["offset"]}&sort=submissiontime%3Adesc',
                headers=self.headers,
                meta={
                    'id' : response.request.meta["id"],
                    'offset' : response.request.meta['offset'] + 100,
                    'retry_count' : 0
                }
            )