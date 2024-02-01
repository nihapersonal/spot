{{ config(materialized = 'table') }}

select DISTINCT song_name, artist_name, played_at, SPOTIFY_UNIQUE_RECORD_KEY,
CONVERT(NVARCHAR(32),HashBytes('MD5',CONCAT(SPOTIFY_UNIQUE_RECORD_KEY,INGESTION_DATE)), 2) 
            AS SPOTIFY_UNIQUE_PER_INGESTION_RECORD_KEY
FROM {{ ref('UNIQUE_RECORD_KEY') }};




