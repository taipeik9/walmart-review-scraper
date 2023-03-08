# Walmart Reviews Scraper and NLP Analysis
An efficient Walmart review scraper using only the Walmart API for any Walmart product category and NLP analysis on the reviews of Walmart products.

This scraper works on Walmart.ca only.

Examples of valid urls, your url should have a similar structure as the following:

**These urls are examples of valid category urls from walmart.ca**

https://www.walmart.ca/browse/beauty/skin-care/facial-cleansers-toners/face-wash/6000198722778-6000195305341-6000195308541-6000198737951?icid=browse_l2_beauty_face_wash_3744_3QFXRBEJOA&fromFC=true

https://www.walmart.ca/browse/beauty/skin-care/face-moisturizers/6000198722778-6000195305341-6000195309547?icid=browse_l2_beauty_face_moisturizers_3743_23HEAAILKN&fromFC=true

**These urls are examples of valid search urls from walmart.ca**

https://www.walmart.ca/search?q=cerave&c=6000198722778

https://www.walmart.ca/search?q=cereal

**This url is an example of a valid brand url from walmart.ca**

https://www.walmart.ca/brand/l-or-al-paris/51036683

Note: None of these links have a page value "p=", the scraper will always start at page one, don't include the page value in the link

To use the scraper, change the url in the command line in the docker-compose.yml file. ex:
```
command: "python3 crawl.py '[url]'"
```

If you want to limit the number of products in the scraper you can use the optional limit argument. This will be an int after the url
```
command: "python3 crawl.py '[url]' [int]"
```
Note: The limit argument is not exact, often it can be over or under by one or two products.

Then just ```docker-compose up``` in the root folder with the ```--build``` flag if this is your first time running the script.

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