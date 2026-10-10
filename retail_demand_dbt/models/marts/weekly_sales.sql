SELECT
    item_id,
    store_id,
    DATE_TRUNC(date, WEEK(SATURDAY)) AS week_start,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,

    SUM(sales) AS total_sales,
    AVG(sales) AS avg_daily_sales,
    MAX(sales) AS max_daily_sales,
    COUNTIF(sales > 0) AS selling_days,
    COUNT(*) AS total_days

FROM {{ ref('daily_sales') }}

WHERE date IS NOT NULL

GROUP BY
    item_id,
    store_id,
    week_start,
    year,
    month