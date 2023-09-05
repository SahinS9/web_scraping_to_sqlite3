import requests
from bs4 import BeautifulSoup
import sqlite3


#user agent to get data
headers = {
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

#empty list in order to add dictionaries in it during scraping
p = []

#loop thru pages of the website within defined range
for x in range(1,21):
    r = requests.get(f'https://www.compusale.az/index.php?route=product/manufacturer/info&manufacturer_id=2&page={x}')
    soup = BeautifulSoup(r.content,  features = 'lxml')
    # print(soup.prettify())
    main = soup.find('div', class_ = "main-products-wrapper")
    productlist = main.find_all('div', class_ = "caption")



#Take needed data from each object to the dictionary and add it to the List
    for x in productlist:
        
       p.append( {'product_code':x.find('span', class_= 'stat-2').find_all('span')[1].string,
          'product_name':x.find('div', class_= 'name').find('a').string,
            'price_inc_vat':x.find('span', class_= 'price-normal').string,
                'price_exc_vat': x.find('span', class_= 'price-tax').string})
    

#print(p)

#Connect to the DB OR Create if it does not exist
conn = sqlite3.connect('products.db')
c = conn.cursor()



#Create table If not exists
c.execute("""
    CREATE Table IF NOT EXISTS products (
          product_code TEXT,
          product_name TEXT,
          price_inc_vat TEXT,
          price_exc_vat TEXT
    )

""")


#INSERT INTO Table one by one in the loop / *BULK INSERT IS BETTER OPTION
def insert_pr(u):
    with conn:
        # print(u)
        # print(u['product_name'])
        c.execute("INSERT INTO products (product_code, product_name, price_inc_vat, price_exc_vat) VALUES (?, ?, ?, ?)",
              (u['product_code'], u['product_name'], u['price_inc_vat'], u['price_exc_vat']) )
        

#call function to insert and start the process in order to use this data in data_cleaning.py to get needed values
for pl in p:
    print(pl)
    print(pl['product_name'])
    insert_pr(pl)


