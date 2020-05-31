import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('assignmentsolution.sqlite')
print("Opened database successfully")
cur = conn.cursor()

cur.execute	('DROP TABLE IF EXISTS Artist')
cur.execute	('DROP TABLE IF EXISTS Genre')
cur.execute	('DROP TABLE IF EXISTS Album')
cur.execute	('DROP TABLE IF EXISTS Track')

cur.executescript('''
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

handler = open('Library.xml').read()
tree = ET.fromstring(handler)
lst = tree.findall('dict/dict/dict')

def lookup(lst, attribute):
    found = False
    for i in lst:
        if found: return i.text
        if i.tag=='key' and i.text == attribute:
            found = True
    return None
for entry in lst: 
    if ( lookup(entry, 'Track ID') is None ) : continue
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    genre = lookup(entry, 'Genre')
    count = lookup(entry, 'Play Count')
    length = lookup(entry, 'Total Time')
    rating = lookup(entry, 'Rating')

    if name is None or artist is None or genre is None or album is None : 
        continue

    #print(name, artist, album, count, rating, length, genre)
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', (artist, ))
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', (genre, ))
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ?)''', 
        ( name, album_id, genre_id, length, rating, count ) )

conn.commit()
#conn.close()
