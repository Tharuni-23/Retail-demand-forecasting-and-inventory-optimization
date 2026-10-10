WITH source_data AS (

    SELECT
        store_id,
        item_id,
        wm_yr_wk,
        sell_price

    FROM {{ source('m5_retail', 'raw_sell_prices') }}

)

SELECT *
FROM source_data