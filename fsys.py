import re
import os

class FileSystem(object):

    def __init__(self, path):
        self.path = path

    def dbc(self):
        dbexists = os.path.exists(self.path)
        return dbexists

    def configc(self):
        dir = re.sub(r'\w*.db$', '', self.path)
        config_path = f'{dir}dircf.txt'

        if os.path.exists(config_path) == True:  # Si existe.
            print('Archivo de configuración encontrado!')
            with open(config_path, 'r') as config:
                lines = []
                for line in config:
                    lines.append(line)
                cf1 = float(lines[0].replace('\n', ''))  # Almacenar valores en una variable
                cf2 = float(lines[1])

        else:  # Si no existe
            print('Archivo de configuración no encontrado')
            with open(config_path, 'w') as config:
                l1 = input("Introduzca el costo por persona:")
                l2 = input("Introduzca el costo por niño:")
                cf1 = float(l1)
                cf2 = float(l2)
                l1 = l1 + '\n'
                lines = [l1, l2]

                for line in lines:
                    config.write(line)

            print('Exito!')

        self.cf1 = cf1
        self.cf2 = cf2

    def getcf(self):
        return self.cf1, self.cf2



