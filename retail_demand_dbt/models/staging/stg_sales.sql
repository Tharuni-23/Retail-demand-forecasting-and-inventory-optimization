WITH source_data AS (

    SELECT
        id,
        item_id,
        store_id,
        d,
        sales

    FROM {{ source('m5_retail', 'sales_validation_long') }}

)

SELECT *
FROM source_data