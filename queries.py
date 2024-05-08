from prettytable import PrettyTable

import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303nle6')


cursor = cnx.cursor()

class Query:
    # outputs top n selling products in each state
    def top_selling_products_by_state(self,n):
        cursor.execute(
            '''
                SELECT 
                    state,
                    item_name,
                    SUM(quantity) AS total_sold
                FROM 
                    stores, ships, orders, order_items, apparel
                WHERE 
                    stores.store_id = ships.store_id
                    AND ships.order_id = orders.order_id
                    AND orders.order_id = order_items.order_id
                    AND order_items.apparel_id = apparel.apparel_id
                GROUP BY 
                    state,
                    item_name
                ORDER BY 
                    state,
                    total_sold DESC
            '''
        )
        items = cursor.fetchall()

        # create table
        table = PrettyTable()
        table.field_names = ["State", "Apparel Name", "Quantity Sold"]

        hashmap = {}
        for item in items:
            state, item_name, total_sold = item
            if state not in hashmap:
                hashmap[state] = 1
            else:
                hashmap[state] += 1
            
            # get top k products in each state
            if hashmap[state] <= n:
                # add rows to the table
                table.add_row([state, item_name, total_sold])
        

        print(table)

    # output n stores with top number of products
    def top_stores_by_product_sold(self,n):
        cursor.execute(
            '''
            SELECT 
                s.store_id,
                CONCAT(s.address, ', ', s.city, ', ', s.state) AS store_location,
                SUM(oi.quantity) AS total_sales
            FROM 
                customer_orders co
                JOIN order_items oi ON co.order_id = oi.order_id
                JOIN ships sh ON co.order_id = sh.order_id
                JOIN stores s ON sh.store_id = s.store_id
            GROUP BY 
                s.store_id, 
                store_location
            ORDER BY 
                total_sales DESC
            LIMIT %s;
            ''', (n, )
        )

        items = cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["Store ID", "Store Location", "Total Products Sold"]
        for item in items:
            store, location, sales = item
            table.add_row([store, location, sales])
        
        print(table)

    # output total revenues for all stores 
    def total_revenue_all_stores_desc(self):
        cursor.execute(
            '''
            SELECT s.store_id,
            CONCAT(s.address, ', ', s.city, ', ', s.state) AS full_address,
            SUM(oi.quantity * a.price) AS total_revenue
            FROM stores s
            LEFT JOIN ships sh ON s.store_id = sh.store_id
            LEFT JOIN order_items oi ON sh.order_id = oi.order_id
            LEFT JOIN apparel a ON oi.apparel_id = a.apparel_id
            GROUP BY s.store_id, full_address
            ORDER BY total_revenue DESC;
            '''
        )

        items = cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["Store ID", "Store Location", "Total Revenue"]
        for item in items:
            store, location, revenue = item
            if not revenue:
                revenue = 0
            table.add_row([store, location, revenue])
        print(table)
    
    # output the stores where item1 outsells item2
    def outsell(self,item1, item2):
        item1_query = f'''
            SELECT s.store_id, COALESCE(COUNT(oi.quantity), 0) AS quantity
            FROM stores s
            LEFT JOIN ships sh ON s.store_id = sh.store_id
            LEFT JOIN orders o ON sh.order_id = o.order_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id AND oi.apparel_id = {item1}
            GROUP BY s.store_id;        
        '''
        cursor.execute(item1_query)

        table1 = cursor.fetchall()
        print(table1)

        item2_query = f'''
            SELECT s.store_id, COALESCE(COUNT(oi.quantity), 0) AS quantity
            FROM stores s
            LEFT JOIN ships sh ON s.store_id = sh.store_id
            LEFT JOIN orders o ON sh.order_id = o.order_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id AND oi.apparel_id = {item2}
            GROUP BY s.store_id;
        '''
        cursor.execute(item2_query)

        table2 = cursor.fetchall()
        print(table2)
        table = PrettyTable()
        table.field_names = ["Store ID",  "Item " + str(item1) + " Quantity", "Item " + str(item2) + " Quantity"]

        for i in range(29): 
            quant1 = table1[i][1]
            quant2 = table2[i][1]
            if quant1 > quant2:
                table.add_row([table1[i][0], quant1, quant2])
        print(table)


    
        # for item in info:
        #     store, item1, item2 = item
        #     if item1 > item2:
        # # return table
        # print(table)
        
    # output top 3 types/categories of product sold
    def top_selling_categories(self):
        query = '''
            SELECT
                'running shoes' AS product_type,
                COUNT(*) AS total_orders
            FROM
                com303fpfm.order_items oi
            INNER JOIN
                running_shoes rs ON oi.apparel_id = rs.apparel_id
            UNION ALL
            SELECT
                'basketball shoes' AS product_type,
                COUNT(*) AS total_orders
            FROM
                com303fpfm.order_items oi
            INNER JOIN
                basketball_shoes bs ON oi.apparel_id = bs.apparel_id
            UNION ALL
            SELECT
                't-shirts' AS product_type,
                COUNT(*) AS total_orders
            FROM
                com303fpfm.order_items oi
            INNER JOIN
                tshirts t ON oi.apparel_id = t.apparel_id
            UNION ALL
            SELECT
                'polos' AS product_type,
                COUNT(*) AS total_orders
            FROM
                com303fpfm.order_items oi
            INNER JOIN
                polos p ON oi.apparel_id = p.apparel_id
            UNION ALL
            SELECT
                'sweatpants' AS product_type,
                COUNT(*) AS total_orders
            FROM
                com303fpfm.order_items oi
            INNER JOIN
                sweatpants sp ON oi.apparel_id = sp.apparel_id
            UNION ALL
            SELECT
                'casual pants' AS product_type,
                COUNT(*) AS total_orders
            FROM
                com303fpfm.order_items oi
            INNER JOIN
                casual_pants cp ON oi.apparel_id = cp.apparel_id
            ORDER BY
                total_orders DESC
            LIMIT 3;
        '''

        cursor.execute(query)

        info = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Apparel Type", " Quantity"]
        for item in info:
            product, quantity = item
            table.add_row([product, quantity])
        # return table
        print(table)

    # output n top_selling products in each store
    def top_selling_products_by_store(self,n):
        query = '''
        SELECT  
            s.store_id, 
            a.apparel_id, 
            a.item_name, 
            SUM(oi.quantity) AS total_sold 
        FROM 
            stores s
        JOIN 
            has h ON s.store_id = h.store_id
        JOIN 
            order_items oi ON h.apparel_id = oi.apparel_id
        JOIN 
            apparel a ON h.apparel_id = a.apparel_id
        GROUP BY 
            s.store_id, a.apparel_id, a.item_name
        ORDER BY
            s.store_id, total_sold DESC'''

        cursor.execute(query)

        info = cursor.fetchall()

        store = 1
        counter = 0
        products_for_store = []
        for (storeid, quantity, name, totalsold) in info:
            #print(storeid, quantity, name, totalsold)
            if storeid == store and counter <= n:
                print(storeid, quantity, name, totalsold)
                products_for_store.append([storeid, quantity, name, totalsold])
                counter += 1
            if counter == n:
                store += 1
                counter = 0
        
        table = PrettyTable()
        table.field_names = ["Store ID", "Apparel ID", "Apparel Name", "Total Sold"]
        for item in products_for_store:
            storeid, item_id, name, totalsold = item
            table.add_row([storeid, item_id, name, totalsold])
        # return table
        print(table)


    # total revenue of online orders for a specific range of time 
    def revenue_online_orders(self, start_time, end_time):
        query = '''
        SELECT 
            s.store_id,
            SUM(o.order_total) AS total_revenue
        FROM 
            stores s, ships sh, online_orders o
        WHERE 
            s.store_id = sh.store_id
            AND sh.order_id = o.order_id
            AND o.order_date >= %s
            AND o.order_date <= %s
        GROUP BY
            s.store_id
        ORDER BY
            s.store_id;
        '''
        cursor.execute(query, (start_time, end_time))

        info = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Store ID", "Online Order Revenue"]
        for (storeid, online_revenue) in info:
            table.add_row([storeid, online_revenue])
        
        print(table)
    
    # total revenue of in person orders for a specific range of time 
    def revenue_inperson_orders(self, start_time, end_time):
        query = '''
        SELECT 
            s.store_id,
            SUM(o.order_total) AS total_revenue
        FROM 
            stores s, ships sh, inperson_orders o
        WHERE 
            s.store_id = sh.store_id
            AND sh.order_id = o.order_id
            AND o.purchase_date >= %s
            AND o.purchase_date <= %s
        GROUP BY
            s.store_id
        ORDER BY
            s.store_id;
        '''
        cursor.execute(query, (start_time, end_time))

        info = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Store ID", "In-person Order Revenue"]
        for (storeid, online_revenue) in info:
            table.add_row([storeid, online_revenue])
        
        print(table)
    
def main():
    query = Query()
    query.outsell(51,42)

if __name__ == "__main__":
    main()


