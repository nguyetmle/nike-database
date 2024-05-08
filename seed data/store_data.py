import random
import faker
import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303fpfm')


cursor = cnx.cursor()

# generate 30 stores
fake = faker.Faker('en_US')

def generate_store(index):
    store = []
    # storeId = fake.unique.random_int(min=1000, max=9999)
    storeId = index
    phone_number = fake.phone_number() 
    address = fake.street_address() 
    city = fake.city() 
    state = fake.state_abbr() 
    
    store.append(storeId)
    store.append(address)
    store.append(city)
    store.append(state)
    store.append(phone_number)


    return store

stores = [generate_store(i) for i in range(1,30)]

for idx, store in enumerate(stores):
    print(f"Store {idx}: {store}")


# insert data

stores = tuple(stores)

for store in stores:
    sql = "INSERT INTO stores(store_id, address, city, state, phone_number) VALUES (%s, %s, %s, %s, %s)"
    val = store[0], store[1], store[2], store[3], store[4]
    cursor.execute(sql, val)

cnx.commit()


