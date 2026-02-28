from datetime import datetime
import os
from os import system
from server import DBTServer

class Interface(object):

    def __init__(self, dbconn, fsys, cf1, cf2): #Constructor de interface a partir del objeto Database previamente creado en la clase main.
        self.dbconn = dbconn
        self.cf1 = cf1
        self.cf2 = cf2

    def interface_init(self):
        prompts = ['Introduzca el nombre de la persona:', #Prompts utilizados durante la operación "Agregar registro"
                   'Introduzca el apellido de la persona:',
                   "Cantidad de personas",
                   'Introduzca la cantidad de niños (0 si ninguno)',
                   'Introduzca el pago cubierto por la persona:']
        attributes = ['ID', 'Nombre', 'Apellido', 'No. Personas', 'No. Niños', 'Total', 'Deuda', 'Pagado', 'Fecha'] #Atributos utilizados durante la operación "Consultar registro"
        print('Interfaz iniciada correctamente!')
        print('\nQue desea hacer?\n')

        deactivator = False #Variable que detiene la interfaz (finaliza el programa)
        while deactivator == False: #(Bucle de funcionamiento de la interfaz)

            print('1)Consultar registro\n2)Agregar registro\n3)Eliminar registro\n5)Abonar\n6)Guardar y salir\n7)Salir sin guardar')
            opt = input() #Opcion por elegir

            if opt == '1':
                self.clear_console()

                fname = input('Introduzca el nombre de la persona:')
                query = self.dbconn.myquery(fname) #Uso del metodo myquery para realizar una consulta

                try:
                    for column, attribute in zip(query[0], attributes): #Obtener los atributos y los valores de la consulta en la base de datos para imprimirlos
                        print(f'{attribute}: {column}')
                    print('Exito!')
                except IndexError: #Atrapar indexerror, el registro no existe
                    print("No existe ese registro")

            elif opt == '2':
                self.clear_console()
                personvalues = [0, 0, 0, 0, 0]
                counter = 0 #Éste contador se utiliza para comprobar que la recolección de datos estuvo completa al contar cuantas veces se le pidió entrada al usuario
                try:
                    for num in range(0, 5):
                        print(prompts[num]) #Imprimir los prompts de acuerdo con el numero de entrada
                        if num < 2:
                            personvalues[num], cancelc = DBTServer.input_val(value_type='string')
                            if cancelc: #Si el metodo string_iv (string_inputvalidation) retorna un true para cancelc (cancelcomprobation), entonces la entrada se cancela.
                                break
                        else:
                            personvalues[num], cancelc = DBTServer.input_val()
                            if cancelc:
                                break

                        counter = counter + 1

                except ValueError as e:
                    print(e)

                if counter < 5: #Si el contador es menos de 6, es decir, se le pidieron menos de 6 entradas al usuario, entonces la entrada es incompleta y se cancela y se cancela para evitar la creación de registros basura
                    print("Entrada cancelada")
                else: #Si el contador es 6, significa que el usurio introdujo exitosamente todos los valores, por lo tanto, se crea el registro en la base de datos
                    total_payment = DBTServer.calc_total(self.cf1, self.cf2, float(personvalues[2]), float(personvalues[3]))
                    debt = DBTServer.calc_debt(total_payment, float(personvalues[4]))
                    self.dbconn.add_reg(personvalues[0], personvalues[1], int(personvalues[2]), int(personvalues[3]), total_payment, debt, float(personvalues[4]), int(datetime.now().timestamp()))
                    print('Exito!')

            elif opt == '3': #Borrado de registro mediante nombre
                self.clear_console()
                fname = input('Introduzca el nombre de la persona:')
                confirmation = input("Introduzca si/no para confirmar o cancelar")
                if confirmation.lower() == 'si':
                    self.dbconn.del_reg(fname)
                    print('Exito')
                elif confirmation.lower() == 'no':
                    print('Cancelado')
                else:
                    print('Se ha introducido otra opción, se ha cancelado por seguridad')

            elif opt == '5':
                print('Introduzca el nombre de la persona')
                try:
                    fname, cancelc = DBTServer.input_val(value_type= 'string')
                except ValueError as e:
                    print(e)
                print('Introduzca la cantidad a abonar')
                try:
                    pay, cancelc = DBTServer.input_val()
                except ValueError as e:
                    print(e)

                self.dbconn.pay(pay, fname)
                print('Exito!')

            elif opt == '6': #Guardar y salir
                self.clear_console()
                self.dbconn.closedb_save()
                deactivator = True

            elif opt == '7': #Salir
                self.clear_console()
                self.dbconn.closedb()
                deactivator = True


    def clear_console(self):
        if os.name == 'nt':
            system('cls')
        else:
            system('clear')

