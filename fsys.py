import re
import sys
import os
from server import DBTServer
import tkinter
from tkinter import messagebox

class FileSystem(object):

    def __init__(self, path, name, manual_path= True): #Crear objeto filesystem a partir de la ruta de la base de datos
        self.name = name
        if os.name == 'nt':
            dir_path = fr'{os.path.expanduser('~')}\OneDrive\Documents\databases\{name}'
        elif os.name == 'posix':
            dir_path = fr'{os.path.expanduser('~')}/databases/{name}'

        if manual_path:
            self.path = path
        else:
            if os.path.exists(dir_path):
                print('Base de datos encontrada!')
            else:
                print('Base de datos no encontrada.')
                os.makedirs(dir_path)
            if os.name == 'nt':
                self.path = fr'{dir_path}\db.db'
            elif os.name == 'posix':
                self.path = fr'{dir_path}/db.db'

        self.line_names = ['adult_value:', 'child_value:', 'disp_format:']

    def dbc(self): #Comprobar si la base de datos existe
        dbexists = os.path.exists(self.path)
        return dbexists

    def configc(self):
        self.dir = re.sub(r'\w*.db$', '', self.path) #Obtener ruta y archivo de configuración de la base de datos en el mismo directorio
        self.config_path = f'{self.dir}dbconfig.txt'
        prompts = ["Introduzca el costo por persona:", "Introduzca el costo por niño:"]

        if os.path.exists(self.config_path):  #Comprobar si existe el archivo de configuración de la base de datos en el mismo directorio.
            print('Archivo de configuración encontrado!')
            if self.config_file_comprobation(self.config_path):
                with open(self.config_path, 'r') as config: #Leer el archivo de configuración si existe.
                    lines = []
                    for line in config: #Leer las líneas de configuración en el archivo
                        lines.append(line[12:]) #Asignar los valores de las líneas a la lista
                    cf1 = float(lines[0].replace('\n', ''))  # Almacenar valores en una variable
                    cf2 = float(lines[1].replace('\n', ''))
                    cf3 = lines[2]
                    self.cf1 = cf1
                    self.cf2 = cf2
                    self.cf3 = cf3
            else:
                root = tkinter.Tk()
                root.withdraw()

                ans = messagebox.askyesno('Error: 033', 'El archivo de configuración está dañado ¿Desea repararlo?')

                if ans:
                    os.remove(self.config_path)
                    print('Archivo de configuración corrupto eliminado!')
                    self.configc()
                else:
                    sys.exit(0)

        else:  # Si no existe
            print('Archivo de configuración no encontrado')
            config_lines = [0, 0, '']
            print() #Introducir líneas de configuración

            counter = 0
            for i in range(2):
                print(prompts[i])
                config_lines[i], cancelc = DBTServer.input_val(cancel_return= True, decimals=True)
                if cancelc:
                    break

                counter = counter + 1

            config_lines[2] = 'list'

            if counter < 2:
                sys.exit(0)
            else:
                cf1 = float(config_lines[0])  # Convertir líneas de configuración a números de punto flotante para su uso en la interfaz
                cf2 = float(config_lines[1])
                cf3 = 'list'
                config_lines[0] = str(cf1)
                config_lines[1] = str(cf2)
                config_lines[0] = config_lines[0] + '\n'  # Separador de líneas para su almacenamiento en el archivo de texto de configuración
                config_lines[1] = config_lines[1] + '\n'
                with open(self.config_path,'w') as config:  # Crear archivo de configuración en el mismo directorio de la base de datos
                    for line_name, config_line in zip(self.line_names, config_lines): #Escribir las líneas de configuración en el archivo creado
                        config.write(fr'{line_name}{config_line}')

                self.cf1 = cf1
                self.cf2 = cf2
                self.cf3 = cf3

            print('Exito!')

    def change_config(self, cf1, cf2, disp_format):
        #Agregar codigo
        config_lines = [str(cf1), str(cf2), disp_format]
        config_lines[0] = config_lines[0] + '\n'  # Separador de líneas para su almacenamiento en el archivo de texto de configuración
        config_lines[1] = config_lines[1] + '\n'
        with open(self.config_path,'w') as config:  # Crear archivo de configuración en el mismo directorio de la base de datos
            for line_name, config_line in zip(self.line_names,config_lines):  # Escribir las líneas de configuración en el archivo creado
                config.write(fr'{line_name}{config_line}')

        self.cf1 = cf1
        self.cf2 = cf2
        self.cf3 = disp_format

    def getcf(self): #Obtener valores de configuración para su uso en otras clases
        return self.cf1, self.cf2, self.cf3

    def config_file_comprobation(self, config_path):
        line_names = ['adult_value', 'child_value', 'disp_format']
        valid_count = 0
        v_total = 3
        with open(config_path, 'r') as config:
            for config_line, line_name in zip(config, line_names):
                if re.fullmatch(fr'{line_name}:\d+\.\d+\n', config_line) != None or re.fullmatch(fr'{line_name}:(list|table)', config_line) != None:
                    valid_count = valid_count + 1

        print(f'Comprobación de archivo de configuración exitosa!\nLineas correctas:{valid_count}\nLineas incorrectas:{v_total - valid_count}')

        if v_total == valid_count:
            proceed = True
        else:
            proceed = False

        return proceed






