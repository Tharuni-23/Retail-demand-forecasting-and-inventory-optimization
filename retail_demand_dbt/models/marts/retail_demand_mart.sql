SELECT
    w.item_id,
    w.store_id,
    w.week_start,
    w.year,
    w.month,
    w.total_sales,
    w.avg_daily_sales,
    w.max_daily_sales,
    w.selling_days,
    w.total_days,

    SAFE_DIVIDE(
        w.selling_days,
        w.total_days
    ) AS selling_day_ratio

FROM {{ ref('weekly_sales') }} AS w