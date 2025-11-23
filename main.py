from DBFunctions import Database
from interface import Interface
from fsys import FileSystem
import re
import os

print(r'''############################################################
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
0.2 By Gsoft''')

opt = input('\nBienvenido a TDATABASER ¿Qué desea hacer?\n1) Crear o conectar a base de datos\n2) Acerca de\n3) Cerrar')
if opt == '1':
    path = input('Introduzca la dirección de de la base de datos existente o por crear:\n')
    print('Inicializando sistema de ficheros...')
    fsys = FileSystem(path)
    print('Exito!')
    db = Database(path)
    print('Comprobación de fichero...')
    dbexists = fsys.dbc()
    if dbexists == True:
        print('Comprobación exitosa!')
        print('Iniciando base de datos...')
        db.create_table()
        print('Exito!')
        print('Buscando archivo de configuración...')
        fsys.configc()
        cf1, cf2 = fsys.getcf()
        print('Iniciando interfaz...')
        interface = Interface(db, cf1, cf2)
        interface.interface_init()
    else:
        print('Error 011: El fichero no existe o la ruta es inválida.')
        print('Saliendo...')
elif opt == '2':
    print('''\nTDATABASER es un software que permite administrar una base de datos SQL relativa
a los registros de los clientes de excursiones turísticas.
    
            Programmer                           Application Desing
    Juan Manuel Sánchez Granados            Juan Manuel Sánchez Granados
    
                            Ver: 0.2  GSoft 2025''')
elif opt == '3':
    print('Saliendo...')
else:
    print('Error 022: Opción inexistente.')