{{ config(materialized = 'view') }}

select song_name,
        artist_name,
        played_at,
        played_on_date,
        RAW_FILE_NAME,
        SPOTIFY_UNIQUE_RECORD_KEY,
        SPOTIFY_UNIQUE_PER_INGESTION_RECORD_KEY,
        INGESTION_DATE,
        INGESTION_DTTM
from {{ ref('staging_final')}}
where INGESTION_DATE >= CAST( GETDATE() AS Date );