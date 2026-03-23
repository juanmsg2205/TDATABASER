class DBTServer():

    @staticmethod
    def calc_total(p_config, c_config, p_quantity, c_quantity):
        total_payment = p_config*p_quantity + c_config*c_quantity
        return total_payment

    @staticmethod
    def calc_debt(total_payment, cov_payment):
        debt = total_payment - cov_payment
        return debt

    @staticmethod
    def input_val(value_type = 'numeric', cancel_return = False):
        if cancel_return == True:
            prompt = 'Introduzca el valor deseado (Introduzca Q para quitar): '
        else:
            prompt = 'Introduzca el valor deseado: '

        valid_t = {'numeric', 'string'}
        if value_type not in valid_t:
            raise ValueError(f"Error: Método input_validation no reconoce {value_type} como argumento válido.")

        elif value_type == 'numeric':
            input_c = False  # Variable que permite comprobar si la entrada es correcta (si lo es se sale del bucle)
            cancel = False  # Variable que permite comprobar si la entrada se canceló (si se canceló se sale del bucle)
            while not input_c and not cancel:
                user_input = input(prompt)
                if user_input.lower() == 'q':  # Si la entrada es q, entonces se cancela la operación, se asigna true para cancel y se sale del bucle
                    cancel = True
                    print('Cancelado')
                elif user_input.isnumeric():  # Se comprueba si la entrada es numérica, se asigna true para input_comprobation y se sale del bucle
                    input_c = True
                else:  # En caso de que la entrada no sea numérica y no se haya cancelado con q, se le indica al usuario el error.
                    print(
                        'Su entrada podría contener carácteres alfabéticos o carácteres especiales, introduzca un valor numérico correcto')

        elif value_type == 'string':
            input_c = False
            cancel = False
            while not input_c and not cancel:
                user_input = input(prompt)
                if user_input.lower() == 'q':
                    cancel = True
                    print('Cancelado')
                elif not user_input.isnumeric():
                    input_c = True
                else:
                    print('Su entrada podría contener números, introduzca un valor alfabético correcto')

        if cancel_return:
            return user_input, cancel
        else:
            return user_input





