import pandas as pd
from pandas.errors import DataError, EmptyDataError


class Exporter(object):

    def __init__(self, fsys, db_conn):
        self.path = fsys.dir
        self.db_conn = db_conn

    def full_query_db(self):
        self.full_query = self.db_conn.get_all()
        self.database_dataframe = pd.DataFrame(self.full_query)
        self.database_dataframe.columns = ['ID', 'Nombre', 'Apellido', 'Cantidad adultos', 'Cantidad niños', 'Deuda',
                                       'Total', 'Pagado', 'Fecha']

    def export(self, name, type = 'excel'):
        valid_types = {'excel', 'csv', 'txt'}
        if type not in valid_types:
            raise ValueError(f'Error: El argumento {type} no se reconoce como un argumento válido')

        try:
            self.full_query_db()
            if type == 'excel':
                path = fr'{self.path}{name}.xlsx'
                self.database_dataframe.to_excel(path, 'database')

            elif type == 'csv':
                path = fr'{self.path}{name}.csv'
                self.database_dataframe.to_csv(path)

            elif type == 'txt':
                attributes = ['ID', 'Nombre', 'Apellido', 'No. Personas', 'No. Niños', 'Total', 'Deuda', 'Pagado',
                              'Fecha']
                path = fr'{self.path}{name}.txt'
                with open(path, 'w') as txt_export:
                    for register in self.full_query:
                        for attribute, feature in zip(attributes, register):
                            line = f'{attribute}: {feature}\n'
                            txt_export.writelines(str(line))
                        txt_export.writelines('\n')

            print(f'Éxito! archivo guardado en la ruta: {path}')

        except(DataError, IndexError, KeyError, EmptyDataError) as e:
            print(e)
