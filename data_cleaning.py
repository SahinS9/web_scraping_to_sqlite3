import pandas as pd
import sqlite3
import re


#Connect to the Database - If it exists
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Query All needed data
df = c.execute("Select * from products").fetchall()

#Create DataFrame with proper column names
df = pd.DataFrame(df, columns = ['code','pr','price_azn','price_exc_vat_azn'])

#Take numerical data out of the columns with regex
df['price_azn'] = df.price_azn.apply(lambda x : re.findall(r'\d+(?:,\d+)?\.\d+', x)[0])
df['price_exc_vat_azn'] = df.price_exc_vat_azn.apply(lambda x : re.findall(r'\d+(?:,\d+)?\.\d+', x)[0])

#Set column type as Float in order to be able to work on it
df.price_azn = df.price_azn.astype('float64')
df.price_exc_vat_azn = df.price_exc_vat_azn.astype('float64')

#Have output in order to report in Excel
df.to_excel('output.xlsx', sheet_name= "web_scraping", index = False)

