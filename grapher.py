import matplotlib.pyplot as plt
import pandas as pd
from pandas.errors import DataError, EmptyDataError
from datetime import datetime

class DBgrapher(object):
    def __init__(self, dbconn):
        self.dbconn = dbconn

    def desc_debt_graph(self):
        try:
            desc_df = pd.DataFrame(self.dbconn.debt_desc())
            desc_df.columns = ['FNAME', 'LNAME', 'DEBT']
            desc_df['FNAME'] = desc_df['FNAME'] + " " + desc_df['LNAME']
            desc_df.drop('LNAME', axis = 1, inplace = True)

            plt.figure(figsize = (12, 6))
            plt.bar(x = desc_df['FNAME'], height = desc_df['DEBT'])
            plt.title(f'Diez Mayores Deudores {datetime.now()}')
            plt.xticks(fontsize = 6)
            plt.xlabel('Nombre')
            plt.ylabel('Cantidad (MXN)')
            plt.show()

        except(DataError, IndexError, KeyError, EmptyDataError) as e:
            print(e)




