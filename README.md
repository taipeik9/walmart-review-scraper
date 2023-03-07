# Walmart Reviews Scraper and NLP Analysis
An efficient Walmart review scraper using only the Walmart API for any Walmart product category and NLP analysis on the reviews of Walmart products.

To use the scraper:
```
scrapy crawl products -o products.json
```

Once the product spider is finished:
```
scrapy crawl reviews -o [filename].csv
```

## Scraping Stats:

This scraper is efficient and fairly simple. It sends request to the Walmart API with the "products" spider for the products on the category pages and then gathers the product info and ids in a json. Then it sends requests to the bazaar API with the "reviews" spider to collect all of the review data and stores it in a csv.

First Test (60 Products):
- Face Moisturizer category
- 961 Total Requests
- ~122 Seconds Elapsed
- 86720 Total Reviews

Second Test (30 Products)
- Skin Care Bestsellers Category
- Didn't record requests or time
- 76800/82171 Reviews Collected, 93.4%
- First Test with crawl.py
- First Test dealing with Rate Limiting (3 Request Retries & No Download Delay)

Third Test (30 Products)
- Skin Care Bestsellers Category
- 1035 Total Requests
- ~212.9 Seconds Elapsed
- 97561/97561 Reviews Collected, 100%
- Rate Limiting (3 Request Retries & 0.1s Download Delay),
- 13 total retries