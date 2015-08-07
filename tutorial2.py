import requests
from threading import Thread

class minuteprice:

    pricelist = []
    
    def __init__(self):
        pass
        
    def getlink(self,stock):
        return('https://www.google.com/finance/getprices?q=%s&x=NASD&i=60&p=1d&f=c' %(stock))
    
    def getprice(self,url):
        r = requests.get(url)
        self.pricelist = r.content.split()[-391:] 
        return 
         
def main():
      
    slist = ['FB','AAPL','GOOG','AMZN','MSFT']
    pricelib = {}        
    thlist = [] 

    for stock in slist:
        pricelib[stock] = minuteprice()
        url = pricelib[stock].getlink(stock) 
        t = Thread(target=pricelib[stock].getprice,args=(url,))
        t.start()
        thlist.append(t)    
    for th in thlist:
        th.join()
        
    for stock in pricelib:
        print stock, pricelib[stock].pricelist

if __name__ =="__main__":
    main()
 
 
    