import random
import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303fpfm')


cursor = cnx.cursor()

primary_key = {}
table = []
for i in range(1000):
    entry = []
    storeId = random.randint(1,29)
    orderId = random.randint(1,100)
    if orderId not in primary_key:
        primary_key[orderId] = storeId
        quantity = random.randint(1, 100)
        entry.append(storeId)
        entry.append(orderId)
    if entry: #in case of empty entry
        table.append(entry)

print(table)
print("Table size: " + str(len(table)))
table = tuple(table)

for entry in table:
    sql = "INSERT INTO ships(store_id, order_id) VALUES (%s, %s)"
    val = entry[0], entry[1]
    cursor.execute(sql, val)

cnx.commit()



