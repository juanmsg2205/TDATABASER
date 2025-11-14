class Interface(object):

    def __init__(self,dbconn):
        self.dbconn = dbconn

    def interface_init(self):
        print('Interfaz iniciada correctamente!')
        print('\nQue desea hacer?\n')

        deactivator = False
        while deactivator == False:

            print('1)Consultar registro\n2)Agregar registro\n3)Eliminar registro\n4)Guardar y salir\n5)Salir sin guardar')
            opt = input()

            if opt == '1':
                fname = input('Introduzca el nombre de la persona:')
                query = self.dbconn.myquery(fname)
                print(query)
                print('Exito!')

            elif opt == '2':
                fname = input('Introduzca el nombre de la persona:')
                lname = input('Introduzca el apellido de la persona:')
                peopleq = int(input('Introduzca la cantidad de personas:'))
                debt = float(input('Introduzca la deuda de la persona:'))
                paid = float(input('Introduzca el pago cubierto por la persona:'))
                date = input("Introduzca la fecha de inicio de contrato:")
                self.dbconn.add_reg(fname, lname, peopleq, debt, paid, date)
                print('Exito!')

            elif opt == '4':
                self.dbconn.closedb_save()
                deactivator = True

            elif opt == '5':
                self.dbconn.closedb()
                deactivator = True





