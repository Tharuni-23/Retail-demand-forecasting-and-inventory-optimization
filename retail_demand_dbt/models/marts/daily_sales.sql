WITH sales AS (

    SELECT *
    FROM {{ ref('stg_sales') }}

),

calendar AS (

    SELECT *
    FROM {{ ref('stg_calendar') }}

)

SELECT
    s.id,
    s.item_id,
    s.store_id,
    s.d,
    c.date,
    c.wm_yr_wk,
    c.weekday,
    c.wday,
    c.month,
    c.year,
    c.event_name_1,
    c.event_type_1,
    c.event_name_2,
    c.event_type_2,
    c.snap_CA,
    c.snap_TX,
    c.snap_WI,
    s.sales

FROM sales AS s

LEFT JOIN calendar AS c
    ON s.d = c.d