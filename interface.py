from datetime import datetime
from server import DBTServer
from exporter import Exporter
from grapher import DBgrapher

class Interface(object):

    def __init__(self, dbconn, fsys, cf1, cf2, config_format, autosave): #Constructor de interface a partir del objeto Database previamente creado en la clase main.
        self.dbconn = dbconn
        self.fsys = fsys
        self.cf1 = cf1
        self.cf2 = cf2
        self.config_format = config_format
        self.autosave = autosave
        self.attributes = ['ID', 'Nombre', 'Apellido', 'No. Personas', 'No. Niños', 'Total', 'Deuda', 'Pagado',
                  'Fecha']  # Atributos utilizados durante la operación "Consultar registro"
        self.dbconn.autosave = self.autosave

    def interface_init(self):
        exporter = Exporter(self.fsys, self.dbconn)
        prompts = ['Introduzca el nombre de la persona:', #Prompts utilizados durante la operación "Agregar registro"
                   'Introduzca el apellido de la persona:',
                   "Cantidad de personas",
                   'Introduzca la cantidad de niños (0 si ninguno)',
                   'Introduzca el pago cubierto por la persona:']

        print('Interfaz iniciada correctamente!')
        print('\nQue desea hacer?\n')

        deactivator = False #Variable que detiene la interfaz (finaliza el programa)
        while deactivator == False: #(Bucle de funcionamiento de la interfaz)

            print('1)Consultar registro\n2)Consulta general\n3)Agregar registro\n4)Eliminar registro\n5)Abonar\n6)Guardar y salir\n7)Salir sin guardar\n8)Ayuda\n9)Exportar\n10)Configuración\n11)Graficar')
            opt = input() #Opcion por elegir

            if opt == '1':
                DBTServer.clear_console()

                fname = input('Introduzca el nombre de la persona:').lower()
                lname = input('Introduzca el apellido de la persona:').lower()
                query = self.dbconn.myquery(fname, lname) #Uso del metodo myquery para realizar una consulta

                try:
                    for column, attribute in zip(query[0], self.attributes): #Obtener los atributos y los valores de la consulta en la base de datos para imprimirlos
                        print(f'{attribute}: {column}')
                    print('Exito!')
                except IndexError: #Atrapar indexerror, el registro no existe
                    print("No existe ese registro")

            elif opt == '2':
                DBTServer.clear_console()
                print(f'BD:{self.fsys.name}     Precio Adulto:{self.fsys.cf1}       Precio Niño:{self.fsys.cf2}\n')
                self.retrieve_all()

            elif opt == '3':
                DBTServer.clear_console()
                personvalues = [0, 0, 0, 0, 0]
                counter = 0 #Éste contador se utiliza para comprobar que la recolección de datos estuvo completa al contar cuantas veces se le pidió entrada al usuario
                try:
                    for num in range(0, 5):
                        print(prompts[num]) #Imprimir los prompts de acuerdo con el numero de entrada
                        if num < 2:
                            personvalues[num], cancelc = DBTServer.input_val(value_type='string', cancel_return=True)
                            if cancelc: #Si el metodo string_iv (string_inputvalidation) retorna un true para cancelc (cancelcomprobation), entonces la entrada se cancela.
                                break
                        elif num == 2 or num == 3:
                            personvalues[num], cancelc = DBTServer.input_val(cancel_return=True, decimals=False)
                            if cancelc:
                                break
                        elif num ==4:
                            personvalues[num], cancelc = DBTServer.input_val(cancel_return=True, decimals=True)
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

            elif opt == '4': #Borrado de registro mediante nombre
                DBTServer.clear_console()
                print('Introduzca el nombre de la persona:')
                fname = DBTServer.input_val(value_type='string', cancel_return=False).lower()
                print('Introduzca el apellido de la persona:')
                lname = DBTServer.input_val(value_type='string', cancel_return=False).lower()
                confirmation = input("Introduzca si/no para confirmar o cancelar")

                if confirmation.lower() == 'si':
                    message  = self.dbconn.del_reg(fname, lname)
                    print(message)
                elif confirmation.lower() == 'no':
                    print('Cancelado')
                else:
                    print('Se ha introducido otra opción, se ha cancelado por seguridad')


            elif opt == '5':
                print('Introduzca el nombre de la persona')
                try:
                    fname= DBTServer.input_val(value_type= 'string', cancel_return=False).lower()

                    print('Introduzca el apellido de la persona')
                    lname = DBTServer.input_val(value_type='string', cancel_return=False).lower()

                    print('Introduzca la cantidad a abonar')
                    pay= DBTServer.input_val(cancel_return=False, decimals=True)
                except ValueError as e:
                    print(e)

                message = self.dbconn.pay(pay, fname, lname)
                print(message)


            elif opt == '6': #Guardar y salir
                self.dbconn.closedb_save()
                deactivator = True

            elif opt == '7': #Salir
                self.dbconn.closedb()
                deactivator = True
            elif opt == '8':
                DBTServer.clear_console()
                info = f'''
1) Permite consultar un registro en específico en la base de datos a partir del nombre y apellido de la persona,
se obtiene la información completa: ID de registro, nombre, apellido, cantidad de personas, cantidad de niños, monto total,
deuda, monto pagado y fecha de registro.
2) Permite realizar una consulta completa de la base de datos, en donde se obtendrán todos los atributos anteriormente
mencionados de cada una de las personas en la base de datos en formato de lista.
3) Agrega un registro en la base de datos. Se le pedirá al usuario que ingrese los valores para cada atributo mencionado
en el punto número 1 a excepción de la deuda y el total, los cuales son calculados automáticamente, puede introducir \033[1mQ\033[0m
para cancelar. Consideraciones importantes: El tercer y cuarto valor solo admite entradas de números enteros, el quinto, soporta
enteros y decimales.
4) Borre un registro específico de la base de datos a partir del nombre y apellido de la persona, se solicita confirmación
de operación al usuario para evitar errores de manejo.
5) Abone una cantidad a la cuenta de la persona a partir del nombre y apellido, después de ejecutar la operación
se recalcularán los montos.
6) Se guardarán los cambios en la base de datos y se saldrá del programa.
7) Se descartarán los cambios en la base de datos y se saldrá del programa.
8) Imprime ayuda.
9)Permite exportar la base de datos en formato .xlsx, .csv y .txt, el archivo se localizará en la misma dirección de la base de datos.
                
Notas adicionales:
- Las funciones "1)Consultar Registro", "4)Eliminar Registro", "5)Abonar" no distinguen
entre mayúsculas o minúsculas, la función "3)Agregar Registro" si lo hace.
                
                            GSoft 2026
                '''
                print(info)
                input('\nPresione enter para continuar')

            elif opt == '9':
                DBTServer.clear_console()
                print('Elija el formato:\n1)Excel\n2)CSV\n3)txt\n')
                opt = input()
                try:
                    if opt =='1':
                        exporter.export(self.fsys.name, type='excel')
                    elif opt =='2':
                        exporter.export(self.fsys.name, type='csv')
                    elif opt == '3':
                        exporter.export(self.fsys.name, type='txt')
                except ValueError as e:
                    print(e)

            elif opt == '10':
                DBTServer.clear_console()
                config_list = [self.cf1, self.cf2, self.config_format, self.autosave]
                config_menu_cancel = False
                while not config_menu_cancel:
                    print(f'1)Precio adulto:{config_list[0]}\n2)Precio niño:{config_list[1]}\n3)Formato consulta:{config_list[2]}\n4)Autoguardado:{config_list[3]}\n5)Salir\n')
                    menu = input()

                    if menu == '1':
                        temp_value, cancelc = self.console_clear_Ivalue()
                        if cancelc:
                            pass
                        else:
                            config_list[0] = float(temp_value)

                    elif menu == '2':
                        temp_value, cancelc = self.console_clear_Ivalue()
                        if cancelc:
                            pass
                        else:
                            config_list[1] = float(temp_value)

                    elif menu == '3':
                        format_deactivator = False
                        while not format_deactivator:
                            config_format = input('Elija el valor:\n1)Lista\n2)Tabla\n')

                            if config_format == '1':
                                config_list[2] = 'list'
                                format_deactivator = True
                            elif config_format == '2':
                                config_list[2] = 'table'
                                format_deactivator = True
                            else:
                                print('Opción inexistente')

                    elif menu == '4':
                        autosave_menu_deactivator = False
                        while not autosave_menu_deactivator:
                            config_autosave = input('Elija el valor\n1)Si\n2)No\n')

                            if config_autosave == '1':
                                config_list[3] = True
                                autosave_menu_deactivator = True
                            elif config_autosave == '2':
                                config_list[3] = False
                                autosave_menu_deactivator = True
                            else:
                                print('Opción inexistente')

                    elif menu == '5':
                        past_config = self.retrieve_config_list()
                        counter = 0
                        for i, config_element in enumerate(config_list):
                            if past_config[i] == config_element:
                                counter = counter + 1

                        if counter == 4:
                            config_menu_cancel = True
                            DBTServer.clear_console()
                        else:
                            decision_deactivation = False
                            while not decision_deactivation:
                                decision = input('Se han encontrado cambios en la configuración, ¿Deseas guardarlos? si/no')

                                if decision.lower() == 'si':
                                    self.fsys.change_config(config_list[0], config_list[1], config_list[2], config_list[3])
                                    self.cf1 = config_list[0]
                                    self.cf2 = config_list[1]
                                    self.config_format = config_list[2]
                                    self.autosave = bool(config_list[3])
                                    self.dbconn.autosave = bool(config_list[3])

                                    print('Cambios guardados!')
                                    config_menu_cancel = True
                                    break

                                elif decision.lower() == 'no':
                                    print('Cambios no guardados')
                                    config_menu_cancel = True
                                    break

                                else:
                                    print('Opción incorrecta')

                    else:
                        print('Inexistente')


            elif opt == '11':
                grapher = DBgrapher(self.dbconn)

                graph_option = input('Seleccione la gráfica:\n1)10 mayores deudores\n2)Pagado VS Total\n3)Pagado VS Deuda Total\n')

                if graph_option == '1':
                    grapher.graph_data('debtors')

                elif graph_option == '2':
                    grapher.graph_data('paid_vs_total')

                elif graph_option == '3':
                    grapher.graph_data('paid_vs_total_all')

                else:
                    print('Opción inexistente')

                DBTServer.clear_console()

            else:
                DBTServer.clear_console()
                print('Opción inexistente')

    def retrieve_all(self):
        valid_parameters = ['list', 'table']
        if self.config_format not in valid_parameters:
            raise ValueError(f'El parámetro {self.config_format} no es un parámetro válido para retreive_all format.')
        else:
            query = self.dbconn.get_all()

        if query == 0:
            print('No hay nada en la base de datos')

        else:
            if self.config_format == 'list':
                for register in query:
                    for i in range(9):
                        print(f'{self.attributes[i]}: {register[i]}')
                    print('')

            else:
                for attribute in self.attributes:
                    print(attribute, end='  ')
                print()

                for register in query:
                    for i in range(9):
                        print(register[i], end='   ')
                    print()

            t_total, d_total, p_total = self.dbconn.get_totals()
            print(f'Total:{t_total}\nDeuda total:{d_total}\nTotal pagado:{p_total}\n')

    def console_clear_Ivalue(self):
        DBTServer.clear_console()
        return DBTServer.input_val(decimals=True, cancel_return=True)

    def retrieve_config_list(self):
        return [self.cf1, self.cf2, self.config_format, self.autosave]







