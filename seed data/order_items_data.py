import random
import mysql.connector
cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303fpfm')


cursor = cnx.cursor()

orders = {}
primary_key = {}
table = []
while len(orders) < 100:
    entry = []
    orderId = random.randint(1,100)
    apparelId = random.randint(1,51)
    # make sure all orders are in the table
    if orderId not in orders:
        orders[orderId] = [apparelId]
    else:
        orders[orderId].append(apparelId)

    # avoid duplicate primary key 
    if (orderId, apparelId) not in primary_key:
        primary_key[(orderId, apparelId)] = 1
        quantity = random.randint(1, 20)
        entry.append(orderId)
        entry.append(apparelId)
        entry.append(quantity)
    if entry: #in case of empty entry
        table.append(entry)

print(table)

table = tuple(table)

for entry in table:
    sql = "INSERT INTO order_items(order_id, apparel_id, quantity) VALUES (%s, %s, %s)"
    val = entry[0], entry[1], entry[2]
    cursor.execute(sql, val)

cnx.commit()



