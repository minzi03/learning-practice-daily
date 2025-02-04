select *
from[dbo].[superstore];

#1 What percentage of total orders were shipped on the same date?
/* the 'cast' function is used to convert the count of same-day shipped orders to a 'float' value */
select count(*) AS TotalOrders, 
	sum(case when ship_date = order_date then 1 else 0 end) as SameShippedOrrders,
	round((cast(sum(case when ship_date=order_date then 1 else 0 end) as float)/count(*))* 100, 2) as PercentageOfTotalOrders
from[dbo].[superstore] 

###TotalOrders	SameShippedOrrders	PercentageOfTotalOrders
###9993	        514	                 5.25

#2. Name top 3 customers with highest total quantities of orders.
/* the 'limit' keyword is not recognized in MS SQL. Instead, we should ust the 'top' kwywaord to limit the number of rows returned by the query. */
select top 3 customer_name as top_3_customers, count(*) as total_orders
from [dbo].[superstore]
group by customer_name
order by total_orders desc

###top_3_customers	total_orders
### Raymond Buch  6
### Sean Millear 5
### Tamara Chand 5

#3. Find the top 5 items with the highest average sales.
select top 5 product_name as top_5_items,  round(avg( sales),2) as average_sales
from[dbo].[superstore]
group by product_name
order by average_sales desc

### top_5_items                                      	average_sales
###Cisco TelePresence System EX90 Videoconferencing Unit	 22638.48
###Canon imageCLASS 2200 Advanced Copier	                 12319.96
###Cubify CubeX 3D Printer Triple Head Print	             7999.98
###3D Systems Cube Printer, 2nd Generation, Magenta	         7149.94
###HP Designjet T520 Inkjet Large Format Printer - 24 Color	 6124.97

#4. Write a query to find the average order value for each customer, and rank the customers by their average order value.
SELECT 
    customer_name,
    avg_sales,
    RANK() OVER (ORDER BY avg_sales DESC) AS prank
FROM (
    SELECT 
        customer_name,
        ROUND(AVG(sales), 2) as avg_sales
    FROM 
        [dbo].[superstore]
    GROUP BY 
        customer_name
) AS Subquery
ORDER BY avg_sales DESC;


#5. Give the name of customers who ordered highest and lowest orders from each city.
/* string_agg function is used to concatenate the customer name into a single string.*/
WITH cte AS (
    SELECT city, 
           customer_name, 
           COUNT(order_id) AS num_orders
    FROM [dbo].[superstore]
    GROUP BY city, customer_name
),
cte2 AS (
    SELECT city, 
           MIN(num_orders) AS lowest_order, 
           MAX(num_orders) AS highest_order
    FROM cte
    GROUP BY city
)
SELECT a.city,
       STRING_AGG(CASE WHEN a.num_orders = b.lowest_order THEN a.customer_name ELSE NULL END, ',') AS lowest_order_customers,
       STRING_AGG(CASE WHEN a.num_orders = b.highest_order THEN a.customer_name ELSE NULL END, ',') AS highest_order_customers
FROM cte a
JOIN cte2 b ON a.city = b.city
WHERE a.num_orders = b.lowest_order OR a.num_orders = b.highest_order
GROUP BY a.city;


#6. What is the most demanded sub-category in the west region?
select top 1 sub_category, sum (quantities) as total_number
from [dbo].[superstore]
where Region = 'West'
group by sub_category
order by total_number desc

### sub_category	total_number
### Binders	        462

#7. Which order has the highest number of items? 
select top 1 order_id, count(*) as total_items
from[dbo].[superstore]
group by order_id
order by total_items desc

###order_id	total_items
###CA-2018-100111	14


#8. Which order has the highest cumulative value?
select top 1 order_id, round(sum(sales),2) as total_sales
from [dbo].[superstore]
group by order_id
order by total_sales desc

###order_id	total_sales
###CA-2015-145317	23661.23

#9. Which segment’s order is more likely to be shipped via first class?
select top 1 segment, count(*) total_number
from[dbo].[superstore]
where ship_mode ='first class'
group by segment
order by total_number desc

###segment	total_number
###Consumer	755

#10. Which city is least contributing to total revenue?
select top 1 city, round(sum(sales),2) as total_revenue
from [dbo].[superstore]
group by city
order by total_revenue

### city	total_revenue
### Abilene	1.39

#11. What is the average time for orders to get shipped after order is placed?
select avg(datediff(day, order_date, ship_date)) as avg_shipping_time
from[dbo].[superstore]

### avg_shipping_time
### 3

#12. Which segment places the highest number of orders from each state and which segment places the largest individual orders from each state?
with cte as
(select state, segment, count(order_id) as total_orders
from[dbo].[superstore]
group by state, segment), 
cte2 as
(select state, max(total_orders) as max_orders
from cte
group by state)
select a.state, a.Segment, a.total_orders
from cte as a
join cte2 as b
on a.state=b.state and a.total_orders=b.max_orders
order by state

with cte as
(select state, segment, round(sum(sales),2) as total_sales
from[dbo].[superstore]
group by state, segment), 
cte2 as
(select state, max(total_sales) as max_sales
from cte
group by state)
select a.state, a.Segment, a.total_sales
from cte as a
join cte2 as b
on a.state=b.state and a.total_sales=b.max_sales
order by state

#13. Find all the customers who individually ordered on 3 consecutive days where each day’s total order was more than 50 in value. **
WITH cte AS (
    SELECT 
        customer_id, 
        customer_name, 
        order_date, 
        ROUND(SUM(sales), 2) as total_sales,
        LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_day,
        LEAD(order_date, 2) OVER (PARTITION BY customer_id ORDER BY order_date) AS n_next_day
    FROM [dbo].[superstore]
    GROUP BY customer_id, customer_name, order_date
    HAVING ROUND(SUM(sales), 2) >= 50
)

SELECT DISTINCT 
    a.customer_name, 
    a.order_date, 
    a.next_day, 
    a.n_next_day
FROM cte AS a
WHERE DATEDIFF(day, a.order_date, a.next_day) = 1 
AND DATEDIFF(day, a.next_day, a.n_next_day) = 1;


#14. Find the maximum number of days for which total sales on each day kept rising.**
/* mysql
with CTE as (
select order_date,round(sum(Sales),2) as 'total_sale'
from techhub.superstore
group by Order_Date
order by 1),
cte2 as
(select a.order_date, b.order_date as next_date, a.total_sale, b.total_sale as next_sale,
row_number() over(order by a.order_date) as 'row_date'
from cte as a
join cte as b
on datediff(b.order_date, a.order_date)=1
where a.total_sale < b.total_sale
order by a.order_date)
select  datediff(max(Order_Date), min(Order_Date))as diff_in_days
from cte2
group by Order_Date - interval row_date day
order by 1 desc
limit 1
*/

### diff_in_days
### 4
