from DBFunctions import Database
from interface import Interface
from fsys import FileSystem

def main():
    print(r'''
    ############################################################
    #                                                          #
    #  _________  ________  ________  _________  ________      #
    # |\___   ___\\   ___ \|\   __  \|\___   ___\\   __  \     #
    # \|___ \  \_\ \  \_|\ \ \  \|\  \|___ \  \_\ \  \|\  \    #
    #      \ \  \ \ \  \ \\ \ \   __  \   \ \  \ \ \   __  \   #
    #       \ \  \ \ \  \_\\ \ \  \ \  \   \ \  \ \ \  \ \  \  #
    #        \ \__\ \ \_______\ \__\ \__\   \ \__\ \ \__\ \__\ #
    #         \|__|  \|_______|\|__|\|__|    \|__|  \|__|\|__| #
    #  ________  ________  ________  _______   ________        #
    # |\   __  \|\   __  \|\   ____\|\  ___ \ |\   __  \       #
    # \ \  \|\ /\ \  \|\  \ \  \___|\ \   __/|\ \  \|\  \      #
    #  \ \   __  \ \   __  \ \_____  \ \  \_|/_\ \   _  _\     #
    #   \ \  \|\  \ \  \ \  \|____|\  \ \  \_|\ \ \  \\  \|    #
    #    \ \_______\ \__\ \__\____\_\  \ \_______\ \__\\ _\    #
    #     \|_______|\|__|\|__|\_________\|_______|\|__|\|__|   #
    #                        \|_________|                      #
    #                                                          #
    ############################################################
    0.5.6 By Gsoft''')
    pathmode = False
    #Menú principal
    opt = input('\nBienvenido a TDATABASER ¿Qué desea hacer?\n1) Crear o conectar a base de datos\n2) Acerca de\n3) Cerrar\n4) Ayuda\n')
    if opt == '1': #Opcion 1: Crear o conectarse a base de datos
        if pathmode == True:
            path = input('Introduzca la dirección de de la base de datos existente o por crear:\n')
            print('Inicializando sistema de ficheros...')
            fsys = FileSystem(path,'none', manual_path=pathmode)  # Creación de un objeto FileSystem con la ruta como argumento, para la administración del archivo de configuración
        else:
            name = input('Introduzca el nombre de la base de datos existente o por crear:')
            print('Inicializando sistema de ficheros...')
            fsys = FileSystem('none',name, manual_path=pathmode)

        print('Exito!')
        db = Database(fsys.path) #Creación de un objeto Database con la ruta como argumento para la conexión o creación con la base de datos
        print('Comprobación de fichero...')
        dbexists = fsys.dbc() #Comprueba si la base de datos existe
        if dbexists == True: #Si existe
            print('Comprobación exitosa!')
            print('Iniciando base de datos...')
            db.create_table() #Crea la tabla principal
            print('Exito!')
            print('Buscando archivo de configuración...')
            fsys.configc() #Busca el archivo de configuración y comprueba su existencia (ver fsys.py)
            cf1, cf2 = fsys.getcf() #Asigna las líneas de configuración a las variables para iniciar la interfaz
            print('Iniciando interfaz...')
            interface = Interface(db, fsys, cf1, cf2, 'list') #Crea la interfaz a partir del objeto Database, fsys y las líneas de configuración
            interface.interface_init() #Inicializa la interfaz
        else:
            print('Error 011: El fichero no existe o la ruta es inválida.')
            print('Saliendo...')
    elif opt == '2':
        print('''\nTDATABASER es un software que permite administrar una base de datos SQL relativa
a los registros de los clientes de excursiones turísticas.
        
                Programmer                           Application Desing
        Juan Manuel Sánchez Granados            Juan Manuel Sánchez Granados
        
                                Ver: 0.5.6  GSoft 2026''')
        input('\nPresione enter para continuar')
    elif opt == '3':
        print('Saliendo...')
    elif opt == '4':
        info = r'''
1)(Modo ruta manual, actualmente inactivo) Escriba la ruta completa donde desee ubicar su base de datos y termine el nombrela db.db, de lo contrario
el programa podrá funcionar con errores o será complicado para usted obtener la ruta del programa. Es importante
la creación de una carpeta específica para guardar su base de datos, ya que el sistema de ficheros creará el archivo
de configuración como dbconfig.txt, este archivo estará ligado a la carpeta, por lo que crear dos bases de datos
en una misma carpeta provocará que ambas utilicen el mismo archivo de configuración.
        
Ejemplo:
C:\Users\Paquito\OneDrive\Documents\base-de-datos\db.db
        
(Modo ruta automática, actualmente activo) Escriba el nombre de su base de datos, se creará automáticamente una carpeta
con el nombre y se guardará la base de datos en la ruta C:\Users\(usuario actual)\Documents\databases. 
        
2)Si desea modificar el monto de los precios de la excursión vaya a la carpeta donde guardó su base de datos
y modifique el archivo dbconfig.txt, la primera línea es el precio por adulto y la segunda, el precio por niño.'''

        print(info)
        input('\nPresione enter para salir')
    else:
        print('Error 022: Opción inexistente.')

if __name__ == '__main__':
    main()
