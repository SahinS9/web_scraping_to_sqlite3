import requests
from bs4 import BeautifulSoup
import sqlite3

baseurl = "https://www.thewhiskyexchange.com/"

headers = {
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

# x = 1

# r = requests.get(f'https://www.compusale.az/index.php?route=product/manufacturer/info&manufacturer_id=2&page={x}')

p = []

for x in range(1,21):
    r = requests.get(f'https://www.compusale.az/index.php?route=product/manufacturer/info&manufacturer_id=2&page={x}')
    soup = BeautifulSoup(r.content,  features = 'lxml')
    # print(soup.prettify())
    main = soup.find('div', class_ = "main-products-wrapper")
    productlist = main.find_all('div', class_ = "caption")



    for x in productlist:
        
       p.append( {'product_code':x.find('span', class_= 'stat-2').find_all('span')[1].string,
          'product_name':x.find('div', class_= 'name').find('a').string,
            'price_inc_vat':x.find('span', class_= 'price-normal').string,
                'price_exc_vat': x.find('span', class_= 'price-tax').string})
    

#print(p)

import sqlite3

conn = sqlite3.connect('products.db')
c = conn.cursor()

c.execute("""
    CREATE Table IF NOT EXISTS products (
          product_code TEXT,
          product_name TEXT,
          price_inc_vat TEXT,
          price_exc_vat TEXT
    )

""")

product_list = []


def insert_pr(u):
    with conn:
        # print(u)
        # print(u['product_name'])
        c.execute("INSERT INTO products (product_code, product_name, price_inc_vat, price_exc_vat) VALUES (?, ?, ?, ?)",
              (u['product_code'], u['product_name'], u['price_inc_vat'], u['price_exc_vat']) )
        
#insert_pr(p[0])
for pl in p:
    print(pl)
    print(pl['product_name'])
    insert_pr(pl)


