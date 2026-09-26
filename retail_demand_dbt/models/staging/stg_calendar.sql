WITH source_data AS (

    SELECT
        date,
        wm_yr_wk,
        weekday,
        wday,
        month,
        year,
        d,
        event_name_1,
        event_type_1,
        event_name_2,
        event_type_2,
        snap_CA,
        snap_TX,
        snap_WI

    FROM {{ source('m5_retail', 'raw_calendar') }}

)

SELECT *
FROM source_data