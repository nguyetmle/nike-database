from queries import Query
from prettytable import PrettyTable
from datetime import datetime, timedelta
import random
import mysql.connector

cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303fpfm')


# display products for a store
def display_menu(store_id):
    cursor = cnx.cursor()
    query = """
        SELECT a.UPC, a.item_name, a.price, a.size, a.color
        FROM apparel a
        JOIN has h ON a.apparel_id = h.apparel_id
        WHERE h.store_id = %s
    """
    cursor.execute(query, (store_id,))
    products = cursor.fetchall()

    if not products:
        print("No products available in this store.")
    else:
        # Create table
        table = PrettyTable()
        table.field_names = ["Apparel No.","UPC","Name", "Price", "Size", "Color"]
        for idx, product in enumerate(products):
            upc, name, price, size, color = product
            table.add_row([idx+1, upc, name, price, size, color])

        # Set alignment for numeric columns
        table.align["Price"] = "r"

        # Print the table
        print("Menu of Products in Store " + str(store_id))
        print(table)
    return


# sign-up form for customers
def sign_up():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    
    cursor = cnx.cursor()
    cursor.execute(
        '''
            select count(*) 
            from users
            where username = %s
        ''', (email,)
    )
    info = cursor.fetchall()

    # validate user info
    while info[0][0] > 0: 
        print("This email already exists.")
        email = input("Enter your email: ")
        cursor.execute(
        '''
            select count(*) 
            from users
            where username = %s
        ''', (email,)
        )
        info = cursor.fetchall()

    # enter info
    password = input("Enter your password: ")
    phone_number = input("Enter your phone number: ")
    address = input("Enter your address: ")
    city = input("Enter your city: ")
    state = input("Enter your state: ")
    membership = True

    cursor.execute(
        '''
            insert into customers 
            values (null,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (first_name, last_name, email, phone_number, address, city, state, membership)
    )

    cursor.execute(
        '''
            insert into users
            values (%s,%s,"C")
        ''', (email, password)
    )
    print("Account created successfully.")
    cnx.commit()
    main()
    return

# display list of available stores in each state
def display_store():
    cursor = cnx.cursor()
    cursor.execute(
        '''
            select store_id, state
            from stores
        '''
    )
    stores = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["Store", "State"]
    for store in stores:
        store_id, state = store
        table.add_row([store_id, state])
    # Print the table
    print("List of Stores Available:")
    print(table)

    choice = input("Enter the store number: ")
    while int(choice) < 1 or int(choice) > 29:
        choice = input("Enter a valid store number: ")

    return choice

def view_order_history(customer_id):
    cursor = cnx.cursor()
    cursor.execute(
        '''
        Select co.order_id, a.UPC, a.item_name, a.size, a.color
        From apparel a, order_items oi, orders o, customer_orders co
        Where co.customer_id = %s
        and co.order_id = o.order_id
        and oi.order_id = o.order_id
        and oi.apparel_id = a.apparel_id
        ''', (customer_id,)
    )
    products = cursor.fetchall()

    if not products:
        print("You have no previous order.")
    else:
        # Create table
        table = PrettyTable()
        table.field_names = ["Order ID", "Apparel UPC","Apparel Name","Size", "Color"]
        for product in products:
            ord_id, upc, name, size, color = product
            table.add_row([ord_id, upc, name, size, color])

        print("Here is your previous order(s): ")
        print(table)

    print("Taking you back to customer menu...")
    print("========================")
    customer_menu(customer_id)
    return

def return_order(customer_id):
    # prompt the customer to enter the order ID to return
    order_id = input("Enter the order ID you want to return: ")

    # validate order id 
    cursor = cnx.cursor()
    cursor.execute(
        '''
        SELECT order_id, order_date, receive_date, order_total
        FROM online_orders
        WHERE order_id = %s AND order_id IN (
            SELECT order_id
            FROM customer_orders
            WHERE customer_id = %s
        )
        ''', (order_id, customer_id)
    )
    order_details = cursor.fetchone()

    # if order details not found or order doesn't belong to the customer
    if not order_details:
        print("Invalid order ID or order doesn't belong to you.")
        customer_menu(customer_id)
        return

    order_id, order_date, receive_date, order_total = order_details

    # Display order details
    print("Order ID:", order_id)
    print("Order Date:", order_date)
    print("Receive Date:", receive_date)
    print("Order Total:", order_total)

    cursor.execute(
        '''
        SELECT a.apparel_id, a.UPC, a.item_name, a.price, a.size, a.color, oi.quantity
        FROM order_items oi
        JOIN apparel a ON oi.apparel_id = a.apparel_id
        WHERE oi.order_id = %s
        ''', (order_id,)
    )
    order_items = cursor.fetchall()

    if order_items:
        print("\nProducts in the order:")
        table = PrettyTable()
        table.field_names = ["Apparel UPC","Apparel Name", "Price","Size", "Color","Quantity"]
        for (apparel_id, apparel_upc, item_name, price, size, color, quantity) in order_items:
            table.add_row([apparel_upc,item_name, price, size, color, quantity])
    print(table)

    # confirm return
    confirm_return = input("Do you want to return this order? (Y/N): ").upper()

    if confirm_return == "Y":

        cursor.execute(
        '''
        SELECT store_id
        FROM ships
        WHERE order_id = %s
        ''', (order_id,)
        )
        store_id = cursor.fetchone()[0]

        # update inventory by adding back into has table
        cursor.execute(
        '''
        SELECT apparel_id, quantity
        FROM order_items
        WHERE order_id = %s
        ''', (order_id,)
        )
        returned_items = cursor.fetchall()
        print(returned_items)

        for apparel_id, quantity in returned_items:
            cursor.execute(
                '''
                UPDATE has
                SET quantity = quantity + %s
                WHERE store_id = %s AND apparel_id = %s
                ''', (quantity, store_id, apparel_id)
            )
        

        # delete order entry from online_orders table
        cursor.execute(
            '''
            DELETE FROM online_orders
            WHERE order_id = %s
            ''', (order_id,)
        )

        # delete order entry from customer_orders table
        cursor.execute(
            '''
            DELETE FROM customer_orders
            WHERE order_id = %s
            ''', (order_id,)
        )
        
        # delete products in order_items table
        cursor.execute(
            '''
            DELETE FROM order_items
            WHERE order_id = %s
            ''', (order_id,)
        )

        # delete order from ships table
        cursor.execute(
            '''
            DELETE FROM ships
            WHERE order_id = %s
            ''', (order_id,)
        )

        # delete order entry from orders table
        cursor.execute(
            '''
            DELETE FROM orders
            WHERE order_id = %s
            ''', (order_id,)
        )

        cnx.commit()

        print("Order has been returned successfully")    
    else:
        print("Return cancelled")
    
    print("========================")
    customer_menu(customer_id)
    return

# customer interface
def customer_menu(customer_id):
    print()
    print("===============")
    print("CUSTOMER MENU")
    print()
    print("Select an option:")
    print("1. Add product to cart")
    print("2. View order history")
    print("3. Return an order")
    print("4. Exit")
    choice = int(input("Enter your choice (1-4): "))
    
    # view order history
    if choice == 2: 
        view_order_history(customer_id)
        
    # return order
    elif choice == 3:
        return_order(customer_id)

    # go back to main page
    elif choice == 4:
        print("Exiting...")
        print("========================")
        main()

    # make a purchase
    else:
        store_id = display_store()
        display_menu(store_id)
        choice = input("Enter Apparel UPC to add product to cart, or 2 to exit: ")
        if choice == "2":
            customer_menu(customer_id) 

        item = choice 
        cart = {} #key-value pair is UPC and quantity
        while True:
            # add products to cart
            if item not in cart:
                cart[item] = 1
            else:
                cart[item] += 1

            print("Product " + item + " added to cart successfully")
            choice = input("Enter Apparel UPC to add product to cart, or 2 to exit: ")

            if choice == "2":
                break
            else:
                item = choice #holds upc of new product

        # show shopping cart
        print(cart)
        table = PrettyTable()
        table.field_names = ["No.", "Item Name", "Size", "Price", "Color", "Quantity"]
        order_value = 0
        for idx,upc in enumerate(cart):
            quantity = cart[upc]
            cursor = cnx.cursor()
            cursor.execute(
                '''
                    select item_name, size, price, color
                    from apparel
                    where UPC = %s
                ''', (upc,)
            )
            product_info = cursor.fetchall()
            print(product_info)
            name, size, price, color = product_info[0]
            table.add_row([idx+1, name, size, price, color, quantity])
            order_value += price * quantity
        print("Products in your cart:" )
        print(table)

        # check out
        print("Your order total is: "+ str(order_value))
        credit_card = input("Please enter your credit card number: ")
        order_date = datetime.now()
        receive_date = order_date + timedelta(days=random.randint(1, 5))

        order_date = order_date.strftime('%Y-%m-%d %H:%M:%S')
        receive_date = receive_date.strftime('%Y-%m-%d %H:%M:%S')
        cursor = cnx.cursor()
        # update orders table
        cursor.execute(
            '''
                insert into orders(order_id, order_total, credit_card)
                values (null, %s, %s)
            ''', (order_value, credit_card)
        )

        cursor.execute(
            '''
                select max(order_id)
                from orders
            '''
        )
        order_id = cursor.fetchall()[0][0]

        # update online_orders table
        cursor.execute(
            '''
                insert into online_orders(order_id, order_total, credit_card, order_date, receive_date)
                values (%s, %s,%s,%s,%s)
            ''', (order_id,order_value, credit_card, order_date, receive_date)
        )

        # update customer_orders table
        cursor = cnx.cursor()
        cursor.execute(
            '''
                insert into customer_orders(customer_id, order_id)
                values (%s,%s)
            ''', (customer_id, order_id)
        )

        # update ships table
        cursor = cnx.cursor()
        cursor.execute(
            '''
                insert into ships(store_id, order_id)
                values (%s,%s)
            ''', (store_id, order_id)
        )

        # update has + order_items tables
        cursor = cnx.cursor()
        # apparel_ids = []
        for upc in cart:
            cursor.execute(
                '''
                    select apparel_id
                    from apparel
                    where UPC = %s
                ''', (upc,)
            )
            apparel_id = cursor.fetchall()[0][0]
            # apparel_ids.append(cursor.fetchall()[0][0])
            quantity = cart[upc]
            cursor.execute(
                '''
                    update has 
                    set quantity = quantity - %s
                    where store_id = %s
                    and apparel_id = %s
                ''', (quantity, store_id, apparel_id)
            )
        
            cursor.execute(
                '''
                    insert into order_items(order_id, apparel_id, quantity)
                    values (%s, %s,%s)
                ''', (order_id, apparel_id, quantity)
            )

            cnx.commit()
        print()
        print("Thank you for your purchase!")
        print("Taking you back to customer menu...")
        print("========================")
        customer_menu(customer_id)

# user login interface
def login():
    # check email in database
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    cursor = cnx.cursor()
    cursor.execute(
        '''
            select user_role 
            from users
            where username = %s
            and user_password = %s
        ''', (email, password)
    )
    info = cursor.fetchall()

    if not info:
        print("Invalid username or password.")
        login()

    elif info[0][0] == "C":
        cursor.execute(
        '''
            select customer_id
            from customers
            where email = %s
        ''', (email,)
        )
        customer_id = cursor.fetchall()[0][0]
        customer_menu(customer_id)
    elif info[0][0] == "A":
        admin_menu()
    

# guest interface to purchase anonymously
def guest_login():
    print()
    print("===============")
    print("GUEST MENU")
    print()
    print("Select an option:")
    print("1. Add product to cart")
    print("2. Exit")
    choice = int(input("Enter your choice (1-2): "))

    # go back to main page
    if choice == 2:
        print("Exiting...")
        print("\n ========================")
        main()
    
    else:
        store_id = display_store()
        display_menu(store_id)
        choice = input("Enter Apparel UPC to add product to cart, or 2 to exit: ")
        if choice == "2":
            guest_login()

        item = choice 
        cart = {} #key-value pair is UPC and quantity
        while True:
            # add products to cart
            if item not in cart:
                cart[item] = 1
            else:
                cart[item] += 1

            print("Product " + item + " added to cart successfully")
            choice = input("Enter Apparel UPC to add product to cart, or 2 to exit: ")

            if choice == "2":
                break
            else:
                item = choice #holds upc of new product

        # show cart
        print(cart)
        table = PrettyTable()
        table.field_names = ["No.", "Item Name", "Size", "Price", "Color", "Quantity"]
        order_value = 0
        for idx,upc in enumerate(cart):
            quantity = cart[upc]
            cursor = cnx.cursor()
            cursor.execute(
                '''
                    select item_name, size, price, color
                    from apparel
                    where UPC = %s
                ''', (upc,)
            )
            product_info = cursor.fetchall()
            print(product_info)
            name, size, price, color = product_info[0]
            table.add_row([idx+1, name, size, price, color, quantity])
            order_value += price * quantity
        # Print the table
        print("Products in your cart:" )
        print(table)

        # check out
        print("Your order total is: "+ str(order_value))
        credit_card = input("Please enter your credit card number: ")
        order_date = datetime.now()
        receive_date = order_date + timedelta(days=random.randint(1, 5))

        order_date = order_date.strftime('%Y-%m-%d %H:%M:%S')
        receive_date = receive_date.strftime('%Y-%m-%d %H:%M:%S')
        cursor = cnx.cursor()
        # update orders table
        cursor.execute(
            '''
                insert into orders(order_id, order_total, credit_card)
                values (null, %s, %s)
            ''', (order_value, credit_card)
        )

        cursor.execute(
            '''
                select max(order_id)
                from orders
            '''
        )
        order_id = cursor.fetchall()[0][0]

        # update online_orders table
        cursor.execute(
            '''
                insert into online_orders(order_id, order_total, credit_card, order_date, receive_date)
                values (%s, %s,%s,%s,%s)
            ''', (order_id,order_value, credit_card, order_date, receive_date)
        )

        # update ships table
        cursor = cnx.cursor()
        cursor.execute(
            '''
                insert into ships(store_id, order_id)
                values (%s,%s)
            ''', (store_id, order_id)
        )

        # update has table
        cursor = cnx.cursor()
        # apparel_ids = []
        for upc in cart:
            cursor.execute(
                '''
                    select apparel_id
                    from apparel
                    where UPC = %s
                ''', (upc,)
            )
            apparel_id = cursor.fetchall()[0][0]
            # apparel_ids.append(cursor.fetchall()[0][0])
            quantity = cart[upc]
            cursor.execute(
                '''
                    update has 
                    set quantity = quantity - %s
                    where store_id = %s
                    and apparel_id = %s
                ''', (quantity, store_id, apparel_id)
            )
        
            cursor.execute(
                '''
                    insert into order_items(order_id, apparel_id, quantity)
                    values (%s, %s,%s)
                ''', (order_id, apparel_id, quantity)
            )

            cnx.commit()
        print()
        print("Thank you for your purchase!")
        print("Taking you back to guest menu...")
        print("\n ========================")
        guest_login()
    

# database admin interface
def admin_menu():
    query = Query()
    print()
    print("===============")
    print("DATABASE ADMIN MENU")
    print()
    print("\nPlease choose an option:")
    print("1. Find top-selling products at each store")
    print("2. Find top-selling products in each state")
    print("3. Find top stores by product sold")
    print("4. Find 3 top-selling product categories over all stores")
    print("5. Find stores that Item A outsell Item B")
    print("6. Find total revenue of in-person orders during a time period")
    print("7. Find total revenue of online orders during a time period")
    print("8. Find total revenue in each store in descending order")
    print("0. Exit")
    
    choice = int(input("Enter your choice (0-8): "))
    
    while choice != 0:
        if choice == 1:
            n = int(input("Enter number of products shown for each store: "))
            query.top_selling_products_by_store(n)
        elif choice == 2:
            n = int(input("Enter number of products shown for each state: "))
            query.top_selling_products_by_state(n)
        elif choice == 3:
            n = int(input("Enter number of stores shown: "))
            query.top_stores_by_product_sold(n)
        elif choice == 4:
            # n = int(input("Enter number of categories shown: "))
            query.top_selling_categories()
        elif choice == 5:
            item_a = input("Enter Item A: ")
            item_b = input("Enter Item B: ")
            query.outsell(item_a, item_b)
        elif choice == 6:
            start_time = input("Enter start time (YYYY/MM/DD HH:MM:SS): ")
            end_time = input("Enter end time (YYYY/MM/DD HH:MM:SS): ")
            query.revenue_inperson_orders(start_time, end_time)
        elif choice == 7:
            start_time = input("Enter start time (YYYY/MM/DD HH:MM:SS): ")
            end_time = input("Enter end time (YYYY/MM/DD HH:MM:SS): ")
            query.revenue_online_orders(start_time, end_time)
        elif choice == 8:
            query.total_revenue_all_stores_desc()
        else:
            print("Invalid choice. Please try again.")
        
        print("\nPlease choose an option:")
        print("1. Find top-selling products at each store")
        print("2. Find top-selling products in each state")
        print("3. Find top stores by product sold")
        print("4. Find top-selling product categories over all stores")
        print("5. Find stores that Item A outsell Item B")
        print("6. Find total revenue of in-person orders during a time period")
        print("7. Find total revenue of online orders during a time period")
        print("8. Find total revenue in each store in descending order")
        print("0. Exit")
        choice = int(input("Enter your choice (0-8): "))

    print("Exiting...")
    print("\n ========================")
    main()

def main():
    print("Welcome to Nike!")
    print()
    print(
        '''
                    ⠀⠀ ⢀⠄⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⡤⠖⠚⠁
        ⠀⣰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⢀⣀⣠⣤⣴⣶⡿⠿⠛⠉⠀⠀
        ⢰⣿⣿⣧⣀⣀⣀⣀⣀⣤⣴⣶⣶⣿⣿⣿⠿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠙⢿⣿⣿⣿⣿⡿⠿⠛⠋⠀⠂⠀⠀⠀⠀⠁⠀
        ⠀⠀⠀⠉⠁⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        '''
    )

    print("\n1. User login ")
    print("2. Sign up")
    print("3. Continue as guest")
    print("4. Exit")

    user_choice = int(input("Enter your choice: "))

    while user_choice != 4:
        if user_choice == 1:
            login()
            break
        elif user_choice == 2:
            sign_up()
            break
        elif user_choice == 3:
            guest_login()
            break
        else:
            print("Invalid choice. Please try again.")
            print("\n1. User login ")
            print("2. Sign up")
            print("3. Continue as guest")
            print("4. Exit")
            user_choice = int(input("Enter your choice: "))

    print("Goodbye!")

if __name__ == "__main__":
    main()




