import requests
import json
from bs4 import BeautifulSoup


class Scrape:

    def __init__(self, URL):
        REQ = requests.Session()
        RESPONSE = REQ.get(URL)
        SOUP = BeautifulSoup(RESPONSE.content, 'html.parser')

        print('Getting Shop ID..')
        SHOP_ID = self.GET_SHOP_ID(SOUP)
        if SHOP_ID == False:
            print('Shop ID not found, try again..')
            return

        print('Getting Product list..')
        GET_PRODUCT = self.GET_PRODUCT(REQ, SHOP_ID)
        if GET_PRODUCT == False:
            print('Product list not found, try again..')
            return

        #
        # PRODUCTS = GET_PRODUCT['data']['products']
        # for product in PRODUCTS:
        #     print('Product name: {}'.format(product['name']))
        #
        # ----------------------------------------------------------
        # Now you can get any products data from the seller
        # Just write a code like above then you either save it on .csv or json format
        #

        print('Saving hTML page..')
        self.SAVE_PAGE(SOUP.prettify())

        print('Complete...')

    def SAVE_PAGE(self, SOUP):
        # Save HTML content to file
        with open('Tokopedia_1.html', 'w') as file:
            return file.write(SOUP)

    def GET_SHOP_ID(self, SOUP):
        try:
            SHOP_ID = SOUP.find('input', {'name': 'shop_id'}).get('value')
            return SHOP_ID
        except:
            return False

    def GET_PRODUCT(self, REQ, SHOP_ID):
        try:
            GET_URL = "https://ace.tokopedia.com/search/product/v3?shop_id={}&rows=80&start=0&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=shop_product".format(
                SHOP_ID
            )

            HEADERS = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }

            GET_PRODUCT = REQ.get(GET_URL, headers=HEADERS)
            RESULT = GET_PRODUCT.json()
            with open('Tokopedia.json', 'w') as file:
                json.dump(RESULT, file)

            return RESULT
        except:
            return False


URL = input('Paste the profile URL here:')
Scrape(URL)
