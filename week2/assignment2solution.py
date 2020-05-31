import sqlite3
import re

conn = sqlite3.connect('assignment2solution.sqlite')
print("Opened database successfully")
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER );')
print("Table created successfully")

filename = "mbox.txt"           #input("Input File name here : ")
handler = open(filename)
for line in handler:
    if line.startswith('From: ') :
        lst = re.findall("@[a-zA-z]+[.[a-z]+",(line.split())[1])
        domain = (lst[0])[1:]
        cur.execute('SELECT count FROM Counts WHERE org = ?',(domain,))
        row = cur.fetchone()
        
        if row is None:
            cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)',(domain,))
        else:
            cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',(domain,))

conn.commit()

conn.close()
