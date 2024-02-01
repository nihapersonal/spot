{{
    config(
    schema='TABLE',
    materialized='incremental',
    unique_key= 'SPOTIFY_UNIQUE_PER_INGESTION_META_ACTION_KEY',
    tags=['SPOTIFY', 'delta'],
)
}}

select SPOTIFY_UNIQUE_RECORD_KEY,
        SPOTIFY_UNIQUE_PER_INGESTION_RECORD_KEY,
        SPOTIFY_UNIQUE_PER_INGESTION_META_ACTION_KEY,
        META_ACTION_CD,
        RAW_FILE_NAME
from {{ ref('INSERT_RECORDS')}}