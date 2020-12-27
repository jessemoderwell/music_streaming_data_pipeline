import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - inserts a single record from a song_data json into songs and artists tables
    """

    # open song file
    df = pd.read_json(filepath, lines=True)
    # replace single quotation in strings with single quotes to avoid sql syntax error
    df['artist_name'] = df['artist_name'].str.replace("'", "''")
    df['title'] = df['title'].str.replace("'", "''")


    # insert song record
    song_data = df[['song_id', 'artist_id', 'year', 'duration', 'title']].values[0]
    cur.execute(song_table_insert.format(*list(song_data)))

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0]
    cur.execute(artist_table_insert.format(*list(artist_data)))


def process_log_file(cur, filepath):
    """
    - inserts all relevant fields from a log_data json into time, users and songplays tables
    """

    # open log file
    df = pd.read_json(filepath, lines=True)
    # replace single quotation in strings with single quotes to avoid sql syntax error
    df['artist'] = df['artist'].str.replace("'", "''")
    df['song'] = df['song'].str.replace("'", "''")

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit = 'ms')

    # insert time data records
    time_data = [(int(ts.timestamp() * 1000), ts.hour, ts.day, ts.week, ts.month, ts.year, ts.weekday()) for ts in t]
    column_labels = (['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday'])
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert.format(*list(row)))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert.format(*list(row)))

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select.format(row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row['ts'], row['userId'], row['level'], songid, artistid, row['sessionId'], row['itemInSession'], row['location'], row['userAgent'])
        cur.execute(songplay_table_insert.format(*songplay_data))


def process_data(cur, conn, filepath, func):
    """
    - gathers all files in the data directory and iterates through process_song_file and process_log_file for each one of them
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - connects to postgres instance, and calles process_data for all files in data/song_data and data/log_data, then closes the connection
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
