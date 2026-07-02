-- ============================================================
-- פרויקט AWS Sales Lakehouse Pipeline
-- שאילתות Athena לדוגמה
-- ============================================================
-- הקובץ הזה מכיל שאילתות SQL לדוגמה עבור Athena.
-- בשלב הזה הקובץ מקומי בלבד.
-- הוא לא יוצר שום דבר ב-AWS ולא עולה כסף.
--
-- בעתיד, אחרי שנעלה את קובץ ה-CSV ל-S3,
-- נוכל להשתמש בשאילתות האלה כדי לנתח את נתוני המכירות.
-- ============================================================


-- ============================================================
-- 1. יצירת Database ב-Athena
-- ============================================================

CREATE DATABASE IF NOT EXISTS sales_lakehouse;


-- ============================================================
-- 2. יצירת טבלה חיצונית מעל קובצי CSV ב-S3
-- ============================================================
-- טבלה חיצונית אומרת שהנתונים עצמם נשמרים ב-S3.
-- Athena רק קוראת את הנתונים לפי הגדרת הטבלה.
--
-- בעתיד צריך להחליף את YOUR_BUCKET_NAME בשם הבאקט האמיתי.

CREATE EXTERNAL TABLE IF NOT EXISTS sales_lakehouse.sales_raw (
    order_id INT,
    customer_id INT,
    customer_segment STRING,
    product_id INT,
    product_name STRING,
    category STRING,
    order_date DATE,
    quantity INT,
    unit_price DOUBLE,
    discount_percent DOUBLE,
    total_amount DOUBLE,
    country STRING,
    sales_channel STRING,
    payment_method STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '"',
    'escapeChar' = '\\'
)
LOCATION 's3://YOUR_BUCKET_NAME/raw/sales/'
TBLPROPERTIES (
    'skip.header.line.count'='1'
);


-- ============================================================
-- 3. הצגת 10 השורות הראשונות
-- ============================================================

SELECT *
FROM sales_lakehouse.sales_raw
LIMIT 10;


-- ============================================================
-- 4. ספירת כמות ההזמנות
-- ============================================================

SELECT
    COUNT(*) AS total_orders
FROM sales_lakehouse.sales_raw;


-- ============================================================
-- 5. סך מכירות לפי מדינה
-- ============================================================

SELECT
    country,
    ROUND(SUM(total_amount), 2) AS total_sales,
    COUNT(*) AS number_of_orders
FROM sales_lakehouse.sales_raw
GROUP BY country
ORDER BY total_sales DESC;


-- ============================================================
-- 6. סך מכירות לפי קטגוריית מוצר
-- ============================================================

SELECT
    category,
    ROUND(SUM(total_amount), 2) AS total_sales,
    COUNT(*) AS number_of_orders
FROM sales_lakehouse.sales_raw
GROUP BY category
ORDER BY total_sales DESC;


-- ============================================================
-- 7. מוצרים מובילים לפי מכירות
-- ============================================================

SELECT
    product_id,
    product_name,
    category,
    ROUND(SUM(total_amount), 2) AS total_sales,
    SUM(quantity) AS total_quantity_sold
FROM sales_lakehouse.sales_raw
GROUP BY
    product_id,
    product_name,
    category
ORDER BY total_sales DESC
LIMIT 10;


-- ============================================================
-- 8. מכירות לפי ערוץ מכירה
-- ============================================================

SELECT
    sales_channel,
    ROUND(SUM(total_amount), 2) AS total_sales,
    COUNT(*) AS number_of_orders
FROM sales_lakehouse.sales_raw
GROUP BY sales_channel
ORDER BY total_sales DESC;


-- ============================================================
-- 9. מכירות לפי חודש
-- ============================================================

SELECT
    DATE_FORMAT(CAST(order_date AS TIMESTAMP), '%Y-%m') AS sales_month,
    ROUND(SUM(total_amount), 2) AS total_sales,
    COUNT(*) AS number_of_orders
FROM sales_lakehouse.sales_raw
GROUP BY DATE_FORMAT(CAST(order_date AS TIMESTAMP), '%Y-%m')
ORDER BY sales_month;


-- ============================================================
-- 10. ממוצע הזמנה לפי סגמנט לקוח
-- ============================================================

SELECT
    customer_segment,
    ROUND(AVG(total_amount), 2) AS average_order_value,
    ROUND(SUM(total_amount), 2) AS total_sales,
    COUNT(*) AS number_of_orders
FROM sales_lakehouse.sales_raw
GROUP BY customer_segment
ORDER BY total_sales DESC;