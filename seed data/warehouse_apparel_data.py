import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303nle6')


cursor = cnx.cursor()

table = []

for i in range(1,52):
    entry = []
    storeId = 1
    apparelId = i
    entry.append(storeId)
    entry.append(apparelId)
    table.append(entry)

print(table)

stores = tuple(table)

for entry in table:
    sql = "INSERT INTO warehouse_stock(warehouse_id, apparel_id) VALUES (%s, %s)"
    val = entry[0], entry[1]
    cursor.execute(sql, val)

cnx.commit()
