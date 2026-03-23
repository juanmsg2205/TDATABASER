import re
import os
import sys
from server import DBTServer

class FileSystem(object):

    def __init__(self, path, name, manual_path= True): #Crear objeto filesystem a partir de la ruta de la base de datos
        if manual_path == True:
            self.path = path
        else:
            dir_path = fr'{os.path.expanduser('~')}\OneDrive\Documents\databases\{name}'
            if os.path.exists(dir_path):
                print('Base de datos encontrada!')
            else:
                print('Base de datos no encontrada.')
                os.makedirs(dir_path)
            self.path = fr'{dir_path}\db.db'

    def dbc(self): #Comprobar si la base de datos existe
        dbexists = os.path.exists(self.path)
        return dbexists

    def configc(self):
        dir = re.sub(r'\w*.db$', '', self.path) #Obtener ruta y archivo de configuración de la base de datos en el mismo directorio
        config_path = f'{dir}dbconfig.txt'
        prompts = ["Introduzca el costo por persona:", "Introduzca el costo por niño:"]

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

            config_lines = [0, 0]
            print() #Introducir líneas de configuración

            counter = 0
            for i in range(2):
                print(prompts[i])
                config_lines[i], cancelc = DBTServer.input_val(cancel_return= True)
                if cancelc:
                    break

                counter = counter + 1

            if counter < 2:
                sys.exit(0)
            else:
                cf1 = float(config_lines[0])  # Convertir líneas de configuración a números de punto flotante para su uso en la interfaz
                cf2 = float(config_lines[1])
                config_lines[0] = config_lines[0] + '\n'  # Separador de líneas para su almacenamiento en el archivo de texto de configuración
                with open(config_path,'w') as config:  # Crear archivo de configuración en el mismo directorio de la base de datos
                    for config_line in config_lines: #Escribir las líneas de configuración en el archivo creado
                        config.write(str(config_line))

            print('Exito!')

        self.cf1 = cf1
        self.cf2 = cf2

    def getcf(self): #Obtener valores de configuración para su uso en otras clases
        return self.cf1, self.cf2



