USE com303fpfm;
-- products in each store in desc order
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
    s.store_id, total_sold DESC;

-- top products in each state in desc order
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
	total_sold DESC;

-- total revenue of online orders for a specific range of time 
SELECT 
	s.store_id,
    SUM(o.order_total) AS total_revenue
FROM 
	stores s, ships sh, online_orders o
WHERE 
	s.store_id = sh.store_id
    AND sh.order_id = o.order_id
	AND o.order_date >= '2023/01/01 00:00:00'
    AND o.order_date <= '2023/12/31 23:59:59'
GROUP BY
	s.store_id
ORDER BY
	s.store_id;
    
-- total revenue of inperson orders for a specific range of time 
SELECT 
	s.store_id,
    SUM(o.order_total) AS total_revenue
FROM 
	stores s, ships sh, inperson_orders o
WHERE 
	s.store_id = sh.store_id
    AND sh.order_id = o.order_id
	AND o.purchase_date >= '2023/01/01 00:00:00'
    AND o.purchase_date <= '2023/12/31 23:59:59'
GROUP BY
	s.store_id
ORDER BY
	s.store_id;

-- top 5 stores that sell the most products 
SELECT 
	s.store_id,
	CONCAT(s.address, ', ', s.city, ', ', s.state) AS store_location,
	SUM(oi.quantity) AS total_products_sold
FROM 
	order_items oi, orders o, ships sh, stores s
WHERE
	oi.order_id = o.order_id
    AND o.order_id = sh.order_id
    AND sh.store_id = s.store_id
GROUP BY 
	s.store_id, 
	store_location
ORDER BY 
	total_products_sold DESC
LIMIT 5;

-- total revenue in each store
SELECT s.store_id,
       CONCAT(s.address, ', ', s.city, ', ', s.state) AS full_address,
       SUM(oi.quantity * a.price) AS total_revenue
FROM stores s
LEFT JOIN com303fpfm.ships sh ON s.store_id = sh.store_id
LEFT JOIN com303fpfm.order_items oi ON sh.order_id = oi.order_id
LEFT JOIN apparel a ON oi.apparel_id = a.apparel_id
GROUP BY s.store_id, full_address
ORDER BY total_revenue DESC;


-- restocking
create event restock
on schedule every 1 day
starts '2024-05-2 00:00:00'
do
update has
set quantity = 100
where quantity < 50;





    
