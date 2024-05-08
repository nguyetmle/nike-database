import random
import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303nle6')


cursor = cnx.cursor()

online = {}
instore = {}
table = []

#online customer-online order
while len(table) < 50:
    entry = []
    customerId = random.randint(1,50)
    orderId = random.randint(1,50)
    if orderId not in online:
        online[orderId] = customerId
        entry.append(customerId)
        entry.append(orderId)
    if entry: #in case of empty entry
        table.append(entry)

#instore customer-instore order
while len(table) < 100:   
    entry = []
    customerId = random.randint(51, 100)
    orderId = random.randint(51,100)
    if orderId not in instore:
        instore[orderId] = customerId
        entry.append(customerId)
        entry.append(orderId)
    if entry: #in case of empty entry
        table.append(entry)

table = tuple(table)
print(table)

for entry in table:
    sql = "INSERT INTO customer_orders(customer_id, order_id) VALUES (%s, %s)"
    val = entry[0], entry[1]
    cursor.execute(sql, val)

cnx.commit()



