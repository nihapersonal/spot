{{ config(materialized = 'view') }}

SELECT song_name,
        artist_name,
        played_at,
        played_on_date,
        INGESTION_DTTM,
        RAW_FILE_NAME,
        CAST(INGESTION_DTTM AS DATE) AS INGESTION_DATE,
CONVERT(NVARCHAR(32), HashBytes('MD5', CONCAT(song_name, artist_name, played_at)), 2) 
            AS SPOTIFY_UNIQUE_RECORD_KEY
FROM dbo.raw;



