from datetime import datetime
import os
from os import system

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

            print('1)Consultar registro\n2)Agregar registro\n3)Eliminar registro\n4)Guardar y salir\n5)Salir sin guardar')
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
                for num in range(0, 5):
                    print(prompts[num]) #Imprimir los prompts de acuerdo con el numero de entrada
                    if num < 2:
                        personvalues[num], cancelc = self.string_iv()
                        if cancelc: #Si el metodo string_iv (string_inputvalidation) retorna un true para cancelc (cancelcomprobation), entonces la entrada se cancela.
                            break
                    else:
                        personvalues[num], cancelc = self.numeric_iv()
                        if cancelc:
                            break

                    counter = counter + 1

                if counter < 5: #Si el contador es menos de 6, es decir, se le pidieron menos de 6 entradas al usuario, entonces la entrada es incompleta y se cancela y se cancela para evitar la creación de registros basura
                    print("Entrada cancelada")
                else: #Si el contador es 6, significa que el usurio introdujo exitosamente todos los valores, por lo tanto, se crea el registro en la base de datos
                    total_payment = float(personvalues[2])*self.cf1 + float(personvalues[3])*self.cf2
                    debt = total_payment - float(personvalues[4])
                    self.dbconn.add_reg(personvalues[0], personvalues[1], personvalues[2], personvalues[3], total_payment, debt, personvalues[4], int(datetime.now().timestamp()))
                    print('Exito!')

            elif opt == '3': #Borrado de registro mediante nombre
                self.clear_console()
                fname = input('Introduzca el nombre de la persona:')
                self.dbconn.del_reg(fname)
                print('Exito')

            elif opt == '4': #Guardar y salir
                self.clear_console()
                self.dbconn.closedb_save()
                deactivator = True

            elif opt == '5': #Salir
                self.clear_console()
                self.dbconn.closedb()
                deactivator = True

    def numeric_iv(self): #integer_inputvalidation, permite comprobar que las entradas sean numericas y realizar la cancelación de la operación
        input_c = False #Variable que permite comprobar si la entrada es correcta (si lo es se sale del bucle)
        cancel = False #Variable que permite comprobar si la entrada se canceló (si se canceló se sale del bucle)
        while not input_c and not cancel:
            integer_input = input("Introduzca el valor deseado (introduzca Q para quitar): ")
            if integer_input.lower() == 'q': #Si la entrada es q, entonces se cancela la operación, se asigna true para cancel y se sale del bucle
                cancel = True
                print('Cancelado')
            elif integer_input.isnumeric(): #Se comprueba si la entrada es numérica, se asigna true para input_comprobation y se sale del bucle
                input_c = True
            else: #En caso de que la entrada no sea numérica y no se haya cancelado con q, se le indica al usuario el error.
                print('Su entrada podría contener carácteres alfabéticos o carácteres especiales, introduzca un valor numérico correcto')
        return integer_input, cancel

    def string_iv(self): #string_inputvalidation, permite comprobar que las entradas sean numericas y realizar la cancelación de la operación, funciona igual que integer_iv pero con lógica inversa
        input_c = False
        cancel = False
        while not input_c and not cancel:
            string_input = input("Introduzca el valor deseado (introduzca Q para quitar): ")
            if string_input.lower() == 'q':
                cancel = True
                print('Cancelado')
            elif not string_input.isnumeric():
                input_c = True
            else:
                print('Su entrada podría contener números, introduzca un valor alfabético correcto')
        return string_input, cancel

    def clear_console(self):
        if os.name == 'nt':
            system('cls')
        else:
            system('clear')








