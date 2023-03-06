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

This scraper is efficient and fairly simple. It sends request to the Walmart API with the "products" spider for the products on the category pages and then gathers the product info and ids in a json. Then it sends requests to the bazaar API with the "reviews" spider to collect all of the review data and stores t in a csv.

First Test (60 Products):
- Face Moisturizer category
- 961 Total Requests
- ~122 Seconds Elapsed
- 86720 Total Reviews
