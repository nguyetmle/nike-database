import random
import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303fpfm')


cursor = cnx.cursor()

primary_key = {}
table = []
for i in range(1500):
    entry = []
    storeId = random.randint(1,29)
    apparelId = random.randint(1,51)
    if (storeId, apparelId) not in primary_key:
        primary_key[(storeId, apparelId)] = 1
        quantity = random.randint(1, 100) #number of 1 particular product in a store is 1-100
        entry.append(storeId)
        entry.append(apparelId)
        entry.append(quantity)
    if entry: #in case of empty entry
        table.append(entry)

print(table)

stores = tuple(table)

for entry in table:
    sql = "INSERT INTO has(store_id, apparel_id, quantity) VALUES (%s, %s, %s)"
    val = entry[0], entry[1], entry[2]
    cursor.execute(sql, val)

cnx.commit()



