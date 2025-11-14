from DBFunctions import Database
from interface import Interface
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
0.1 By Gsoft''')

opt = input('\nBienvenido a TDATABASER ¿Qué desea hacer?\n1) Crear o conectar a base de datos\n2) Acerca de\n3) Cerrar')
if opt == '1':
    path = input('Introduzca la dirección de de la base de datos existente o por crear:\n')
    db = Database(path)
    dbexists = os.path.exists(path)
    print('Comprobación de fichero...')
    if dbexists == True:
        print('Comprobación exitosa!')
        print('Iniciando base de datos...')
        db.create_table()
        print('Exito!')
        print('Iniciando interfaz...')
        interface = Interface(db)
        interface.interface_init()
    else:
        print('Error 011: El fichero no existe o la ruta es inválida.')
        print('Saliendo...')
elif opt == '2':
    print('''\nTDATABASER es un software que permite administrar una base de datos SQL relativa
a los registros de los clientes de excursiones.
    
            Programmer                           Application Desing
    Juan Manuel Sánchez Granados            Juan Manuel Sánchez Granados
    
                            Ver: 0.1  GSoft 2025''')
elif opt == '3':
    print('Saliendo...')
else:
    print('Error 022: Opción inexistente.')