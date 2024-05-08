import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303nle6')


cursor = cnx.cursor()

cursor.execute(
    '''
        INSERT INTO warehouse
        VALUES (1)
    '''
)

cnx.commit()