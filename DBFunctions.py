import sqlite3 as sql

class Database(object):

    def __init__(self, dbpath): #Creación de objeto Database a partir de la ruta de la base de datos
        self.dbpath = dbpath
        self.conn = sql.connect(self.dbpath) #Conectar a la base de datos
        self.cursor = self.conn.cursor() #Inicializar el cursosr de la base de datos

    def create_table(self): #Declaración para la creación de la tabla
        script = '''CREATE TABLE IF NOT EXISTS Excursion(
        ID INTEGER PRIMARY KEY NOT NULL,
        FNAME VARCHAR(20),
        LNAME VARCHAR(20),
        PEOPLEQ SMALLINT,
        CHILDQ SMALLINT,
        TOTAL FLOAT,
        DEBT FLOAT,
        PAID FLOAT,
        DATE TIMESTAMP)'''
        self.cursor.execute(script)

    def add_reg(self, fname, lname, peopleq, childq, total, debt, paid, date): #Declaracíon para la creación de un nuevo registro
        script = f'INSERT INTO Excursion(FNAME, LNAME, PEOPLEQ, CHILDQ, TOTAL, DEBT, PAID, DATE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(script, (fname, lname, peopleq, childq, total, debt, paid, date))

    def del_reg(self, fname): #Declaración para eliminar el registro
        script = f'DELETE FROM Excursion WHERE FNAME IN (?)'
        self.cursor.execute(script, (fname,))

    def myquery(self, fname): #Query para obtener un registro a partir del nombre de la persona
        fname = fname.lower()
        script = f'SELECT ID, FNAME, LNAME, PEOPLEQ, CHILDQ, TOTAL, DEBT, PAID, strftime("%d-%m-%Y",DATE, "unixepoch") FROM Excursion WHERE LOWER(FNAME) = ?'
        self.cursor.execute(script, (fname,))
        query = self.cursor.fetchall()
        return query

    def getquery(self): #Retornar query
        query = self.cursor.fetchall()
        return query

    def pay(self, pay, fname):
        script = 'UPDATE Excursion SET PAID = PAID + ? WHERE FNAME = ?'
        self.cursor.execute(script, (pay, fname))
        self.update_debt(fname)

    def update_debt(self, fname):
        script = 'UPDATE Excursion SET DEBT = TOTAL - PAID WHERE FNAME = ?'
        self.cursor.execute(script, (fname,))

    def closedb(self): #Cerrar la conexión con la base de datos sin guardar
        self.conn.close()

    def closedb_save(self): #Guardar y cerrar la conexión con la base de datos
        self.conn.commit()
        self.conn.close()


