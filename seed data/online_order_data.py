import random
import faker
from datetime import timedelta
import mysql.connector

# connect sql
cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303fpfm')

cursor = cnx.cursor()

# generate 50 online orders
fake = faker.Faker()

def generate_online_order(index):
    order = []
    # orderId = fake.unique.random_int(min=1000, max=9999)
    orderId = index
    order_value = random.randint(30,2000)
    credit_card_no = fake.credit_card_number()
    order_date = fake.date_time_between(start_date="-2y", end_date="now")
    receive_date = order_date + timedelta(days=random.randint(1, 5))
    order_date = order_date.strftime("%Y/%m/%d %H:%M:%S")
    
    order.append(orderId)
    order.append(order_value)
    order.append(credit_card_no)
    order.append(order_date)
    order.append(receive_date)
    
    return order

online_orders = [generate_online_order(i) for i in range(1,51)]

for idx, order in enumerate(online_orders, start=1):
    print(f"Customer {idx}: {order}")

online_orders = tuple(online_orders)

for order in online_orders:
    sql = "INSERT INTO orders(order_id, order_total, credit_card) VALUES (%s, %s, %s)"
    val = order[0],order[1],order[2]
    cursor.execute(sql,val)

for order in online_orders:
    sql = "INSERT INTO online_orders(order_id, order_total, credit_card, order_date, receive_date) VALUES (%s, %s, %s, %s, %s)"
    val = order[0],order[1],order[2],order[3],order[4]
    cursor.execute(sql,val)

cnx.commit()


    