import mechanize
from bs4 import BeautifulSoup
import urlparse
import csv

def Crawlglassdoor(maxpage,keyword):
    
    br = mechanize.Browser() 
    br.addheaders = [('User-agent','Mozilla/5.0')]
    br.set_handle_robots(False)
    
    base_url = 'http://www.glassdoor.com' 
    
    
    with open('_'.join(keyword.split(' '))+'_jobs.csv', 'w') as csvfile:       
        fieldnames = ['title', 'company','address','desc']
        writer = csv.DictWriter(csvfile, 
                                fieldnames=fieldnames, 
                                delimiter=',', 
                                lineterminator='\n')
    
        writer.writeheader()
    
        for i in range(maxpage):
        
            p = i+1 
         
            url = 'http://www.glassdoor.com/Job/%s-jobs-SRCH_KO0,%d_IP%d.htm' %('-'.join(keyword.split(' ')),len(keyword),p)
            soup = BeautifulSoup(br.open(url).read())
                        
            for job in soup.find_all('li',{'class':'tbl fill jobListing padHorz hover'}):
                try:
                    item = {}        
                    link = urlparse.urljoin(base_url, job.find('a',{'class':'jobLink'}).get('href'))
                    item['company'] = job.find('span', {'class':'name openScope link plain'}).text
                    item['address'] = job.find('span', {'itemprop':'addressLocality'}).text
                    jobsoup = BeautifulSoup(br.open(link).read())
                    item['title'] = jobsoup.find('h2', {'class':'noMargTop margBotSm strong'}).text
                    item['desc'] = jobsoup.find('div', {'class':'jobDescriptionContent desc notranslate'}).get_text().encode('ascii','ignore')
                    print item
                    writer.writerow(item)
                except:
                    pass
                
    csvfile.close()
    
         
Crawlglassdoor(10, 'data science')
        








