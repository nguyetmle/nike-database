import mysql.connector

# connect sql
cnx = mysql.connector.connect(user='com303nle6', password='nl2520nl',
                              host='136.244.224.221',
                              database='com303fpfm')

cursor = cnx.cursor()



# product(id, upc, name, size, color, price)
cursor.execute(
    '''
        INSERT INTO apparel(apparel_id, UPC, item_name, size, color, price)
        VALUES 
            (1, '10012345601', "Nike Dri-FIT Men's Training T-Shirt", 'M', 'Black', 30), 
            (2, '10012345602', "Nike Dri-FIT Men's Training T-Shirt", 'L', 'Blue', 30),
            (3, '10012345603', "Nike Dri-FIT Men's Training T-Shirt", 'XL', 'Red', 30),
            (4, '20078901201', "Nike Sportswear Women's Essential T-Shirt", 'S', 'White', 25),  
            (5, '20078901202', "Nike Sportswear Women's Essential T-Shirt", 'M', 'Black', 25),
            (6, '20078901203', "Nike Sportswear Women's Essential T-Shirt", 'L', 'Gray', 25),
            (7, '30034567801', "Nike Pro Men's Long Sleeve Training Top", 'S', 'Blue', 35),    
            (8, '30034567802', "Nike Pro Men's Long Sleeve Training Top", 'M', 'Green', 35),   
            (9, '30034567803', "Nike Pro Men's Long Sleeve Training Top", 'L', 'Black', 35),   
            
            (10, '40012345601', "Nike Dri-FIT Victory Men's Golf Polo Shirt", 'M', 'Red', 45),   
            (11, '40012345602', "Nike Dri-FIT Victory Men's Golf Polo Shirt", 'L', 'White', 45),   
            (12, '40012345603', "Nike Dri-FIT Victory Men's Golf Polo Shirt", 'XL', 'Blue', 45),   
            (13, '50090123401', "NikeCourt Advantage Men's Tennis Polo", 'S', 'Navy', 40),    
            (14, '50090123402', "NikeCourt Advantage Men's Tennis Polo", 'M', 'Black', 40),    
            (15, '50090123403', "NikeCourt Advantage Men's Tennis Polo", 'L', 'Gray', 40),    
            (16, '60023456701', "Nike Golf Dry Victory Stripe Polo Shirt", 'M', 'Green', 50),    
            (17, '60023456702', "Nike Golf Dry Victory Stripe Polo Shirt", 'L', 'Black', 50),   
            (18, '60023456703', "Nike Golf Dry Victory Stripe Polo Shirt", 'XL', 'Blue', 50),    
            
            (19, '70045678901', "Nike Sportswear Club Fleece Men's Joggers", 'M', 'Gray', 60),    
            (20, '70045678902', "Nike Sportswear Club Fleece Men's Joggers", 'L', 'Black', 60),    
            (21, '70045678903', "Nike Sportswear Club Fleece Men's Joggers", 'XL', 'Navy', 60),    
            (22, '80023456701', "Nike Therma Men's Training Pants", 'S', 'Green', 70),    
            (23, '80023456702', "Nike Therma Men's Training Pants", 'M', 'Blue', 70),    
            (24, '80023456703', "Nike Therma Men's Training Pants", 'L', 'Black', 70),    
            (25, '90067890101', "Nike Sportswear Tech Fleece Women's Pants", 'S', 'Pink', 75),    
            (26, '90067890102', "Nike Sportswear Tech Fleece Women's Pants", 'M', 'Purple', 75),    
            (27, '90067890103', "Nike Sportswear Tech Fleece Women's Pants", 'L', 'Orange', 75),    
            (28, '10045678901', "Nike Sportswear Tech Fleece Men's Joggers", 'M', 'Yellow', 80),    
            (29, '10045678902', "Nike Sportswear Tech Fleece Men's Joggers", 'L', 'Black', 80),    
            (30, '10045678903', "Nike Sportswear Tech Fleece Men's Joggers", 'XL', 'Gray', 80),    
            (31, '10045678904', "Nike Sportswear Tech Fleece Men's Joggers", 'XXL', 'Green', 80),    
            (32, '10045678905', "Nike Sportswear Tech Fleece Men's Joggers", '3XL', 'Blue', 80),    
            
            (33, '11023456701', "Nike Women's Woven High-Rise Pants", 'S', 'Brown', 85),    
            (34, '11023456702', "Nike Women's Woven High-Rise Pants", 'M', 'Beige', 85),    
            (35, '11023456703', "Nike Women's Woven High-Rise Pants", 'L', 'Khaki', 85),    
            (36, '12090123401', "Nike Men's Cargo Pants", 'S', 'Olive', 90),    
            (37, '12090123402', "Nike Men's Cargo Pants", 'M', 'Tan', 90),    
            (38, '12090123403', "Nike Men's Cargo Pants", 'L', 'Burgundy', 90),    
            (39, '12090123404', "Nike Men's Cargo Pants", 'XL', 'Mustard', 90),    
            (40, '12090123405', "Nike Men's Cargo Pants", 'XXL', 'Slate', 90),    
            (41, '13045678901', "Nike Men's El Chino Pant", '28', 'Navy', 95),    
            (42, '13045678902', "Nike Men's El Chino Pant", '30', 'Charcoal', 95),    
            (43, '13045678903', "Nike Men's El Chino Pant", '32', 'Tan', 95),    
            (44, '13045678904', "Nike Men's El Chino Pant", '34', 'Olive', 95),    
            (45, '13045678905', "Nike Men's El Chino Pant", '36', 'Beige', 95),
            
            (46, '14045678901', "Nike LeBron 18 Basketball Shoes", '10', 'Red', 200),    
            (47, '14045678902', "Nike KD 14 Basketball Shoes", '9', 'Blue', 180),    
            (48, '14045678903', "Nike Kyrie 8 Basketball Shoes", '11', 'Black', 170),   

            (49, '14045678904', "Nike Air Zoom Pegasus 38 Running Shoes", '8', 'Gray', 150),    
            (50, '14045678905', "Nike Zoom Fly 3", '9', 'Black', 120),    
            (51, '14045678906', "Nike ZoomX Invincible Run Flyknit Running Shoes", '7', 'Blue', 180)
    '''
)


# shirt(id, arm sleeve length)
cursor.execute(
    '''
        INSERT INTO shirts
        VALUES
            (1, 'Short'),
            (2, 'Short'),
            (3, 'Short'),
            (4, 'Short'),
            (5, 'Short'),
            (6, 'Short'),
            (7, 'Long'),
            (8, 'Long'),
            (9, 'Long'),
            (10, 'Long'),
            (11, 'Long'),
            (12, 'Long'),
            (13, 'Short'),
            (14, 'Short'),
            (15, 'Short'),
            (16, 'Short'),
            (17, 'Short'),
            (18, 'Short')
    '''
)



# t-shirt(id, neck style)
cursor.execute(
    '''
        INSERT INTO tshirts
        VALUES
            (1, 'Crew'),
            (2, 'Crew'),
            (3, 'Crew'),
            (4, 'V-neck'),
            (5, 'V-neck'),
            (6, 'V-neck'),
            (7, 'Crew'),
            (8, 'Crew'),
            (9, 'Crew')
    '''
)


# polos(id, collar type)
cursor.execute(
    '''
        INSERT INTO polos
        VALUES 
            (10, 'Spread'),
            (11, 'Spread'),
            (12, 'Spread'),
            (13, 'Flat'),
            (14, 'Flat'),
            (15, 'Flat'),
            (16, 'Button-down'),
            (17, 'Button-down'),
            (18, 'Button-down')
    '''
)

# pants(waist size)
cursor.execute(
    '''
        INSERT INTO pants
        VALUES
            (19, 32),
            (20, 34),
            (21, 36),
            (22, 30),
            (23, 32),
            (24, 34),
            (25, 28),
            (26, 30),
            (27, 32),
            (28, 32),
            (29, 34),
            (30, 36),
            (31, 38),
            (32, 40),
            (33, 28),
            (34, 30),
            (35, 32),
            (36, 28),
            (37, 30),
            (38, 32),
            (39, 34),
            (40, 36),
            (41, 28),
            (42, 30),
            (43, 32),
            (44, 34),
            (45, 36)

    '''
)

# sweatpants(drawstring)
cursor.execute(
    '''
        INSERT INTO sweatpants
        VALUES
            (19, True),
            (20, True),
            (21, True),
            (22, False),
            (23, False),
            (24, False),
            (25, False),
            (26, False),
            (27, False),
            (28, True),
            (29, True),
            (30, True),
            (31, True),
            (32, True)

    '''
)


# casual pants(fit style)
cursor.execute(
    '''
        INSERT INTO casual_pants
        VALUES
            (33, 'Relaxed'),
            (34, 'Relaxed'),
            (35, 'Relaxed'),
            (36, 'Slim Fit'),
            (37, 'Slim Fit'),
            (38, 'Slim Fit'),
            (39, 'Slim Fit'),
            (40, 'Slim Fit'),
            (41, 'Straight'), 
            (42, 'Straight'),
            (43, 'Straight'),
            (44, 'Straight'),
            (45, 'Straight')
    '''
)
  


#shoes(material)
cursor.execute(
    '''
        INSERT INTO shoes
        VALUES
            (46, "Synthetic"),
            (47, "Synthetic"),
            (48, "Synthetic"),
            (49, "Mesh"),
            (50, "Mesh"),
            (51, "Flyknit")

    '''
)


# basketball shoes(player brand)
cursor.execute(
    '''
        INSERT INTO basketball_shoes
        VALUES
            (46, "LeBron James"),
            (47, "Kevin Durant"),
            (48, "Kyrie Irving")

    '''
)
# running shoes(distance)
cursor.execute(
    '''
        INSERT INTO running_shoes
        VALUES
            (49, 'Long Distance'),
            (50, 'Short Distance'),
            (51, 'Long Distance')

    '''
)



cnx.commit()


