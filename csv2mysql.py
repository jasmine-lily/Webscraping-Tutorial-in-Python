import csv
import pymysql

f = open('databasepassword.txt')
pwd = f.read().split('\n')
db = pymysql.connect(host = pwd[0], 
                     port = int(pwd[1]), 
                     user = pwd[2], 
                     passwd = pwd[3], 
                     db = pwd[4]
                     )
cursor = db.cursor()

csvf = csv.DictReader(open('companylist.csv','rb'))

for row in csvf:
    print row['Symbol'],row['Name'],row['IPOyear'],row['Sector'],row['Industry']
    cursor.execute('INSERT INTO company VALUES (%s,%s,%s,%s,%s)',
                   (row['Symbol'],
                    row['Name'],
                    int(row['IPOyear'].replace('n/a','0')),
                    row['Sector'],
                    row['Industry'])
                   )
      
cursor.execute('SELECT COUNT(*) FROM company')
count = cursor.fetchone()[0]
print count



