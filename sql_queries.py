# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = ("""create table if not exists songplays (songplay_id varchar, start_time bigint, user_id int, level varchar, song_id varchar, artist_id varchar, location varchar, user_agent varchar, primary key(songplay_id))
""")

user_table_create = ("""create table if not exists users (user_id int, first_name varchar, last_name varchar, gender varchar, level varchar, primary key (user_id))
""")

song_table_create = ("""create table if not exists songs (song_id varchar, title varchar, artist_id varchar, year int, duration numeric, primary key (song_id))
""")

artist_table_create = ("""create table if not exists artists (artist_id varchar, name varchar, location varchar, latitude numeric, longitude numeric, primary key (artist_id))
""")

time_table_create = ("""create table if not exists time (start_time bigint, hour int, day int, week int, month int, year int, weekday int)
""")

# INSERT RECORDS

songplay_table_insert = ("""insert into songplays (start_time, user_id, level, song_id, artist_id, songplay_id, location, user_agent) values ({}, {}, '{}', '{}', '{}', concat('{}', '{}'), '{}', '{}') on conflict (songplay_id) do nothing
""")

user_table_insert = ("""insert into users (user_id, first_name, last_name, gender, level) values ('{}', '{}', '{}', '{}', '{}') on conflict (user_id) do nothing
""")

song_table_insert = ("""insert into songs (song_id, artist_id, year, duration, title) values ('{}', '{}', {}, {}, '{}')
""")

artist_table_insert = ("""insert into artists (artist_id, name, location, latitude, longitude) values ('{}', '{}', '{}', '{}', '{}') on conflict (artist_id) do nothing
""")


time_table_insert = ("""insert into time (start_time, hour, day, week, month, year, weekday) values ({}, {}, {}, {}, {}, {}, {})
""")

# FIND SONGS

song_select = ("""select s.song_id, s.artist_id from songs s join artists a on s.artist_id = a.artist_id
where s.title = '{}'
and a.name = '{}'
and s.duration = {};""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]