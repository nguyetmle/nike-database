create table customers(
customer_id INT AUTO_INCREMENT PRIMARY KEY,
first_name varchar(50),
last_name varchar(50),
email varchar(100) NOT NULL,
phone_number varchar(50),
address varchar(255),
city varchar(50),
state varchar(50),
membership boolean
);

create table stores(
store_id INT auto_increment primary key,
address varchar(255) NOT NULL,
city varchar(50) NOT NULL,
state varchar(50) NOT NULL,
phone_number varchar(20) NOT NULL
);

create table apparel(
apparel_id INT auto_increment primary key,
UPC varchar(100) NOT NULL,
item_name varchar(50),
size varchar(20),
price decimal(10,2),
color varchar(50)
);

create table shirts(
apparel_id INT primary key,
foreign key(apparelid) references apparel(apparelid),
arm_sleeve_length varchar(20)
);

create table tshirts(
apparel_id INT primary key,
foreign key(apparel_id) references shirts(apparel_id),
neck_style varchar(20)
);

create table polos(
apparel_id INT primary key,
foreign key(apparel_id) references shirts(apparel_id),
collar_type varchar(20)
);

create table shoes(
apparel_id INT primary key,
foreign key(apparel_id) references apparel(apparel_id),
material varchar(20)
);

create table runningshoes(
apparel_id INT primary key,
foreign key(apparelid) references shoes(apparel_id),
distance varchar(100)
);

create table basketballshoes(
apparel_id INT primary key,
foreign key(apparelid) references shoes(apparelid),
player_brand varchar(100)
);

create table pants(
apparel_id INT primary key,
foreign key(apparel_id) references apparel(apparel_id),
waist_size varchar(20)
);

create table sweatpants(
apparel_id INT primary key,
foreign key(apparelid) references pants(apparelid),
drawstring boolean
);

create table casualpants(
apparel_id INT primary key,
foreign key(apparel_id) references pants(apparel_id),
fit_style varchar(100)
);

create table orders(
order_id int auto_increment primary key,
order_total decimal(10, 2),
credit_card varchar(50)
);

create table com303fpfm.online_orders(
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_total DECIMAL(10,2),
    credit_card VARCHAR(50),
    order_date TIMESTAMP,
    receive_date TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    INDEX(order_total), -- Adding index
    INDEX(credit_card) -- Adding index
);

create table com303fpfm.inperson_orders(
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_total DECIMAL(10,2),
    credit_card VARCHAR(50),
    purchase_date TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    INDEX(order_total), -- Adding index
    INDEX(credit_card) -- Adding index
);

create table warehouse(
warehouse_id int auto_increment primary key
);

create table com303fpfm.customer_orders(
customer_id int NOT NULL,
order_id int NOT NULL,
PRIMARY KEY (customer_id, order_id),
foreign key(customer_id) references customers(customer_id),
foreign key(order_id) references orders(order_id)
);

create table com303fpfm.ships(
store_id int NOT NULL,
order_id int NOT NULL,
PRIMARY KEY (store_id, order_id),
foreign key(store_id) references stores(store_id),
foreign key(order_id) references orders(order_id)
);

create table com303fpfm.has(
store_id int NOT NULL,
apparel_id int NOT NULL,
quantity int NOT NULL,
PRIMARY KEY (store_id, apparel_id),
foreign key(store_id) references stores(store_id),
foreign key(apparel_id) references apparel(apparel_id)
);

create table com303fpfm.order_items(
    order_id INT NOT NULL,
    apparel_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, apparel_id), -- Composite primary key
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(apparel_id) REFERENCES apparel(apparel_id)
);

create table warehouse_stock(
warehouse_id int NOT NULL,
apparel_id int NOT NULL,
foreign key(warehouse_id) references warehouse(warehouse_id),
foreign key(apparel_id) references apparel(apparel_id)
);

