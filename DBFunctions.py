import sqlite3 as sql

class Database(object):

    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.conn = sql.connect(self.dbpath)
        self.cursor = self.conn.cursor()

    def create_table(self):
        script = '''CREATE TABLE IF NOT EXISTS Excursion(
        ID INTEGER PRIMARY KEY NOT NULL,
        FNAME VARCHAR(20),
        LNAME VARCHAR(20),
        PEOPLEQ SMALLINT,
        DEBT FLOAT,
        PAID FLOAT,
        DATE DATE)'''
        self.cursor.execute(script)

    def add_reg(self, fname, lname, peopleq, debt, paid, date):
        script = f'INSERT INTO Excursion(FNAME, LNAME, PEOPLEQ, DEBT, PAID, DATE) VALUES ("{fname}","{lname}","{peopleq}", "{debt}", "{paid}", "{date}")'
        self.cursor.execute(script)

    def del_reg(self, fname):
        script = f'DELETE FROM Excursion WHERE FNAME IN "{fname}"'
        self.cursor.execute(script)

    def myquery(self, fname):
        fname = fname.lower()
        script = f'SELECT * FROM Excursion WHERE LOWER(FNAME) = "{fname}"'
        self.cursor.execute(script)
        query = self.cursor.fetchall()
        return query

    def getquery(self):
        query = self.cursor.fetchall()
        return query

    def closedb(self):
        self.conn.close()

    def closedb_save(self):
        self.conn.commit()
        self.conn.close()


