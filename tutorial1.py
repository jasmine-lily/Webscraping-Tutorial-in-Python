import requests
from bs4 import BeautifulSoup
import csv

url = 'http://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY&ns=1'

# r is a response object which contains the information of the web page

r = requests.get(url)

# transform the content of r into format which can be processed by
# the functions of BeautifulSoup

soup = BeautifulSoup(r.content)

searchlist = soup.find_all('li',{"class":"regular-search-result"})

with open('restaurant.csv', 'w') as csvfile:
    fieldnames = ['name', 'address','phone','rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    
    writer.writeheader()

    for item in searchlist:
        itemres = {}
        itemres['name'] = item.contents[1].find('a',{"class":"biz-name"}).text.encode('ascii','ignore')
        itemres['address'] = item.contents[1].find('address').text.strip()
        itemres['phone'] = item.contents[1].find('span',{"class":"biz-phone"}).text.strip()
        itemres['rating'] = item.contents[1].find('div',{"class":"rating-large"}).find('i').get('title')
        writer.writerow(itemres)
      
csvfile.close()