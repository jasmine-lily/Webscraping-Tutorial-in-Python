import requests
from bs4 import BeautifulSoup

url = 'http://twittercounter.com/pages/100'
r = requests.get(url)
soup = BeautifulSoup(r.content)
namels = []
for acc in soup.find_all('div',{'class':'name-bio'}):
    namels.append(acc.find('a',{'class':'name'}).text)
   
with open('twitter100.txt','a') as f:   
    for name in namels:
        try:
            print name
            f.write(str(name+'\n'))
        except:
            pass
f.close()












    

    


