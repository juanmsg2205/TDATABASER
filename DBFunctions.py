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
        DEBT FLOAT,
        PAID FLOAT,
        DATE DATE)'''
        self.cursor.execute(script)

    def add_reg(self, fname, lname, peopleq, debt, paid, date): #Declaracíon para la creación de un nuevo registro
        script = f'INSERT INTO Excursion(FNAME, LNAME, PEOPLEQ, DEBT, PAID, DATE) VALUES ("{fname}","{lname}","{peopleq}", "{debt}", "{paid}", "{date}")'
        self.cursor.execute(script)

    def del_reg(self, fname): #Declaración para eliminar el registro
        script = f'DELETE FROM Excursion WHERE FNAME IN ("{fname}")'
        self.cursor.execute(script)

    def myquery(self, fname): #Query para obtener un registro a partir del nombre de la persona
        fname = fname.lower()
        script = f'SELECT * FROM Excursion WHERE LOWER(FNAME) = "{fname}"'
        self.cursor.execute(script)
        query = self.cursor.fetchall()
        return query

    def getquery(self): #Retornar query
        query = self.cursor.fetchall()
        return query

    def closedb(self): #Cerrar la conexión con la base de datos sin guardar
        self.conn.close()

    def closedb_save(self): #Guardar y cerrar la conexión con la base de datos
        self.conn.commit()
        self.conn.close()


