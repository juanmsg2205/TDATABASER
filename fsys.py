import re
import os

class FileSystem(object):

    def __init__(self, path): #Crear objeto filesystem a partir de la ruta de la base de datos
        self.path = path

    def dbc(self): #Comprobar si la base de datos existe
        dbexists = os.path.exists(self.path)
        return dbexists

    def configc(self):
        dir = re.sub(r'\w*.db$', '', self.path) #Obtener ruta y archivo de configuración de la base de datos en el mismo directorio
        config_path = f'{dir}dircf.txt'

        if os.path.exists(config_path) == True:  #Comprobar si existe el archivo de configuración de la base de datos en el mismo directorio.
            print('Archivo de configuración encontrado!')
            with open(config_path, 'r') as config: #Leer el archivo de configuración si existe.
                lines = []
                for line in config: #Leer las líneas de configuración en el archivo
                    lines.append(line) #Asignar los valores de las líneas a la lista
                cf1 = float(lines[0].replace('\n', ''))  # Almacenar valores en una variable
                cf2 = float(lines[1])

        else:  # Si no existe
            print('Archivo de configuración no encontrado')
            with open(config_path, 'w') as config: #Crear archivo de configuración en el mismo directorio de la base de datos
                l1 = input("Introduzca el costo por persona:") #Introducir líneas de configuración
                l2 = input("Introduzca el costo por niño:")
                cf1 = float(l1) #Convertir líneas de configuración a números de punto flotante para su uso en la interfaz
                cf2 = float(l2)
                l1 = l1 + '\n' #Separador de líneas para su almacenamiento en el archivo de texto de configuración
                lines = [l1, l2]

                for line in lines: #Escribir las líneas de configuración en el archivo creado
                    config.write(line)

            print('Exito!')

        self.cf1 = cf1
        self.cf2 = cf2

    def getcf(self): #Obtener valores de configuración para su uso en otras clases
        return self.cf1, self.cf2



