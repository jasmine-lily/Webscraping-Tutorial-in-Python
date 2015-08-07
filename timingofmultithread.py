import requests,time
from threading import Thread

slist = ['FB','AAPL','GOOG','AMZN','MSFT']

def getlink(stock):
    return('https://www.google.com/finance/getprices?q=%s&x=NASD&i=60&p=1d&f=c' %(stock))

def getprice(stock):
    url = getlink(stock)
    r = requests.get(url)
    print r.content.split()[-390:-1] 
    
def sthread(slist):
    for stock in slist:
        getprice(stock)
        
def mthread(slist):    
    thlist = [] 
    for stock in slist:
        t = Thread(target=getprice,args=(stock,))
        t.start()
        thlist.append(t)    
    for th in thlist:
        th.join()
    
def rtime(fn,sl):
    start = time.time()
    fn(sl)
    end = time.time()
    return(end-start)
    
def main():
    print rtime(sthread,slist)
    print rtime(mthread,slist)

if __name__ =="__main__":
    main()
    
    
    