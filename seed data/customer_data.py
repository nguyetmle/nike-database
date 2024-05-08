import random
import faker
import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303nle6')


cursor = cnx.cursor()

fake = faker.Faker('en_US')

def generate_customer(id):
    customer = []
    # required fields
    customerId = id
    email = fake.email()  

    # nonrequired fields
    membership = random.choice([True, False])

    first_name = fake.first_name() if membership  else None
    last_name = fake.last_name() if membership else None
    phone_number = fake.phone_number() if membership else None
    address = fake.street_address() if membership else None
    city = fake.city() if membership else None
    state = fake.state_abbr() if membership else None
    
    customer.append(customerId)
    customer.append(email)
    customer.append(first_name)
    customer.append(last_name)
    customer.append(phone_number)
    customer.append(address)
    customer.append(city)
    customer.append(state)
    customer.append(membership)

    return customer

# generate 50 online customers
online_customers = [generate_customer(i) for i in range(1, 51)]

# generate 50 in-store customers
instore_customers = [generate_customer(i) for i in range(51, 101)]

for idx, customer in enumerate(online_customers + instore_customers, start=1):
    print(customer)


# insert data

instore_customers = tuple(instore_customers)
online_customers = tuple(online_customers)


for customer in online_customers:
    sql = "INSERT INTO customers(customer_id, email, first_name, last_name, phone_number, address, city, state, membership) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6], customer[7],customer[8]
    cursor.execute(sql, val)

for customer in instore_customers:
    sql = "INSERT INTO customers(customer_id, email, first_name, last_name, phone_number, address, city, state, membership) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6], customer[7],customer[8]
    cursor.execute(sql, val)

cnx.commit()


    
    


