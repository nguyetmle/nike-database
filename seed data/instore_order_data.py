import faker
from datetime import timedelta
import random
import faker
from datetime import timedelta
import mysql.connector

# connect sql
cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303nle6')

cursor = cnx.cursor()
fake = faker.Faker()

def generate_instore_order(index):
    order = []
    # orderId = fake.unique.random_int(min=1000, max=9999)
    orderId = index
    order_value = random.randint(30,2000)
    credit_card_no = fake.credit_card_number()
    purchase_date = fake.date_time_between(start_date="-2y", end_date="now")
    purchase_date = purchase_date.strftime("%Y/%m/%d %H:%M:%S")
    
    order.append(orderId)
    order.append(order_value)
    order.append(credit_card_no)
    order.append(purchase_date)
    
    return order


# generate 50 instore orders
instore_orders = [generate_instore_order(i) for i in range(51,101)]

for idx, order in enumerate(instore_orders, start=1):
    print(f"Customer {idx}: {order}")


online_orders = tuple(instore_orders)

for order in instore_orders:
    sql = "INSERT INTO orders(order_id, order_total, credit_card) VALUES (%s, %s, %s)"
    val = order[0],order[1],order[2]
    cursor.execute(sql,val)

for order in instore_orders:
    sql = "INSERT INTO inperson_orders(order_id, order_total, credit_card, purchase_date) VALUES (%s, %s, %s, %s)"
    val = order[0],order[1],order[2],order[3]
    cursor.execute(sql,val)

cnx.commit()



    
    