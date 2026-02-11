CREATE DATABASE food_delivery_db;

# Identify Top-Spending Customers
SELECT Customer_ID,SUM(Final_Amount) AS total_spent
FROM orders
GROUP BY Customer_ID
ORDER BY total_spent DESC
LIMIT 10;

# age group vs order values
SELECT CASE
WHEN Customer_Age < 25 THEN 'Under 25'
WHEN Customer_Age BETWEEN 25 AND 35 THEN '25–35'
WHEN Customer_Age BETWEEN 36 AND 45 THEN '36–45'
ELSE '46+'
END AS age_group,
ROUND(AVG(Order_Value), 2) AS avg_order_value
FROM orders
GROUP BY age_group;

# weekend & weekday
SELECT Order_Day,COUNT(*) AS total_orders
FROM orders
GROUP BY Order_Day;

#monthly revenue trend
SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS month,SUM(Final_Amount) AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month;

# impact discounts on profit
SELECT Discount_Applied,ROUND(AVG(Profit_Margin), 2) AS avg_profit
FROM orders
GROUP BY Discount_Applied;

# high revenue  cuisines
SELECT City,Cuisine_Type,SUM(Final_Amount) AS total_revenue
FROM orders
GROUP BY City, Cuisine_Type
ORDER BY total_revenue DESC;

#average time delivery by cities
SELECT City,ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time
FROM orders
GROUP BY City
ORDER BY avg_delivery_time;

# distance vs delivery delay analysis
SELECT ROUND(Distance_km, 1) AS distance_bucket,ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time
FROM orders
GROUP BY distance_bucket
ORDER BY distance_bucket;

# delivery rating vs delivery time
SELECT ROUND(Delivery_Time_Min, -1) AS delivery_time_range,ROUND(AVG(Delivery_Rating), 2) AS avg_rating
FROM orders
GROUP BY delivery_time_range
ORDER BY delivery_time_range;

# top rated restaurants
SELECT Restaurant_Name,ROUND(AVG(Restaurant_Rating), 2) AS avg_rating
FROM orders
GROUP BY Restaurant_Name
ORDER BY avg_rating DESC
LIMIT 10;

#cancellation rate by restaurants
SELECT Restaurant_Name,COUNT(*) AS cancelled_orders
FROM orders
WHERE Order_Status = 'Cancelled'
GROUP BY Restaurant_Name
ORDER BY cancelled_orders DESC;

# cuisines wise performance 
SELECT Cuisine_Type,COUNT(*) AS total_orders,ROUND(AVG(Restaurant_Rating), 2) AS avg_rating
FROM orders
GROUP BY Cuisine_Type
ORDER BY total_orders DESC; #  high quality cuisines

# delivery partner allocation
SELECT Peak_Hour,COUNT(*) AS total_orders
FROM orders
GROUP BY Peak_Hour;

# payment method preferance 
SELECT Payment_Mode,COUNT(*) AS total_orders
FROM orders
GROUP BY Payment_Mode
ORDER BY total_orders DESC;

# cancellation reason analysis
SELECT Cancellation_Reason,COUNT(*) AS total_cancellations
FROM orders
WHERE Order_Status = 'Cancelled'
GROUP BY Cancellation_Reason
ORDER BY total_cancellations DESC;
# repeated customers
SELECT Customer_ID,COUNT(*) AS order_count
FROM orders
GROUP BY Customer_ID
HAVING order_count > 1
ORDER BY order_count DESC;

























