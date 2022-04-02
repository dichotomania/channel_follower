from bs4 import BeautifulSoup
import requests

url='https://www.youtube.com/watch?v=k8BBSaHf6iI'

re_t = requests.get(url)

soup_t = BeautifulSoup(re_t.text,'lxml')
print(soup_t)

Published =soup_t.find('span',{'id':'dot'})

Time = '時間'
print( Published)



#%%
import psycopg2
from sqlalchemy import create_engine
# engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
# df.to_sql('table_name', engine)

'''
# host="localhost"
dbENGINE= 'django.db.backends.postgresql' #postgresql
dbname='d7rqrbot9jdphg' #資料庫名稱
user='cvyycoqolturzq' #資料庫帳號
password='3d2686d07472f4f90309cfd61672c663195b7eb176cc848da37c6dab2c7d1731' #資料庫密碼
host='ec2-44-194-113-156.compute-1.amazonaws.com'
PORT='5432'
sslmode='allow'
'''

conn=psycopg2.connect(host='ec2-44-194-113-156.compute-1.amazonaws.com',
                     user='cvyycoqolturzq',
                     dbname='d7rqrbot9jdphg',
                     password='3d2686d07472f4f90309cfd61672c663195b7eb176cc848da37c6dab2c7d1731',
                     sslmode='allow'    )

print("Connection complepte")

conn.autocommit = True  #就不用寫 commit 囉con.set_session(autocommit=True)

cursor = conn.cursor()


# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS inventory;")
print("Finished dropping table (if existed)")

# # Create a table
cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
print("Finished creating table")

# # Insert some data into the table
# cursor.execute("INSERT INTO linebotapp_video_info(name, quantity) VALUES (%s, %s);", ("banana", 150))
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
print("Inserted 3 rows of data")

# Fetch all rows from table
print('*****寫入資料庫*****')
cursor.execute("SELECT * FROM inventory;")
rows = cursor.fetchall()

# Print all rows
for row in rows:
    print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))


cursor.close()
conn.close()