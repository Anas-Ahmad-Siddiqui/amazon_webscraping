from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import sys
import json
import psycopg2
import time

"""
Database hosted on ElephantSQL
Database Information
Table Name : moisture_level
Columns : time, moisture 
"""
start = time.time()             # starting time

# establishing the connection
conn = psycopg2.connect(database="kqcryzlv", user='kqcryzlv', password='q7j_jhYG0vq9PeTwLKDMUqBSHdvek0Y_', host='tai.db.elephantsql.com', port='5432')
# Creating a cursor object using the cursor() method
cursor = conn.cursor()

list = []


def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string
        title_string = title_value.strip().replace(',', '')
    except AttributeError:
        return False
    return title_string


def get_price(soup):
    try:
        price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()
    except AttributeError:
        price = ""
    if(price == "(0%)" or price == "0% (0%)"):              # this value is received when the product is out of stock and price isn't displayed
        return "Not Available"
    return price


def get_image(soup):
    try:
        img_div = soup.find(id="img-canvas")
        img_str = img_div.img.get('src')
    except AttributeError:
        img_str = ""
    return img_str


path = os.path.join(sys.path[0], "Amazon Scraping.xlsx")        # Getting the path of the script and adding the file name

df = pd.read_excel(path)

asin = df['Asin'].tolist()              # converting the Asin column of excel sheet to a list
country = df['country'].tolist()        # converting the country  column of excel sheet to a list

for i in range(0, len(asin)):
    if(type(asin[i]) == float or type(asin[i]) == int):
        amazon_link = "https://www.amazon." + country[i] + '/dp/' + str(int(asin[i]))
    elif(type(asin[i]) == str):
        amazon_link = "https://www.amazon." + country[i] + '/dp/' + asin[i]

    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(amazon_link, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "lxml")

    if(webpage.status_code == 404):
        print(amazon_link, "not available")

    else:
        title = get_title(soup)
        if (title == False):
            print(amazon_link, "not available")
            continue

        price = get_price(soup)
        img = get_image(soup)

        title = title.replace("\'", "''")

        data_to_insert = '\'' + title + '\'' + ',' + '\'' + img + '\'' + ',' + '\'' + price + '\''
        cursor.execute("INSERT INTO amazon_scraped_data (title, image_link, price) VALUES ( %s )" % (data_to_insert))
        cursor.execute("commit;")

        dict = {"Product Title": title, "Product Image URL": img, "Price of the Product": price}
        
        list.append(dict)

json_string = json.dumps(list, indent=4)        # creating a json object

path = os.path.join(sys.path[0], "details.json")
with open(path, "w") as outfile:                # writing the json object to a file
    outfile.write(json_string)

end = time.time()           # ending time

print("Time taken to complete the execution:", end - start, "seconds")