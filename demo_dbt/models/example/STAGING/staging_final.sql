select u.song_name,u.artist_name, u.played_at,u.played_on_date, u.INGESTION_DATE,u.RAW_FILE_NAME, 
        s.SPOTIFY_UNIQUE_PER_INGESTION_RECORD_KEY,
        u.INGESTION_DTTM,
        s.SPOTIFY_UNIQUE_RECORD_KEY
from {{ ref('UNIQUE_RECORD_KEY') }} as u
join {{ ref('staging') }} as s 
on u.SPOTIFY_UNIQUE_RECORD_KEY = s.SPOTIFY_UNIQUE_RECORD_KEY