import matplotlib.pyplot as plt
import pandas as pd
from pandas.errors import DataError, EmptyDataError
from datetime import datetime

class DBgrapher(object):
    def __init__(self, dbconn):
        self.dbconn = dbconn

    def graph_data(self, kind):
        try:
            if kind == 'debtors':
                desc_df = pd.DataFrame(self.dbconn.debt_desc_g())
                desc_df.columns = ['FNAME', 'LNAME', 'DEBT']
                desc_df['FNAME'] = desc_df['FNAME'] + " " + desc_df['LNAME']
                desc_df.drop('LNAME', axis = 1, inplace = True)

                plt.figure(figsize = (12, 6))
                bar = plt.bar(x = desc_df['FNAME'], height = desc_df['DEBT'])
                plt.title(f'Diez Mayores Deudores {datetime.now()}')
                plt.xticks(fontsize = 6)
                plt.xlabel('Nombre')
                plt.ylabel('Cantidad (MXN)')
                plt.bar_label(bar, padding = 1)
                plt.show()

            elif kind == 'paid_vs_total':
                pt_df = pd.DataFrame(self.dbconn.debt_vs_paid())
                pt_df.columns = ['FNAME', 'LNAME', 'TOTAL', 'PAID']
                pt_df['FNAME'] = pt_df['FNAME'] + ' ' + pt_df['LNAME']
                pt_df.drop('LNAME', axis = 1, inplace = True)

                plt.figure(figsize =(12, 6))
                plt.bar(x = pt_df['FNAME'], height = pt_df['TOTAL'], color = 'red', label = 'Total')
                plt.bar(x = pt_df['FNAME'], height = pt_df['PAID'], color = 'blue', label = 'Pagado')
                plt.title(f'Pagado VS Total {datetime.now()}')
                plt.xticks(fontsize = 6)
                plt.xlabel('Nombre')
                plt.ylabel('Cantidad (MXN)')
                plt.legend()
                plt.show()

            elif kind == 'paid_vs_total_all':
                full_total, debt_total, paid_total = self.dbconn.get_totals()
                totals_arr = (round(debt_total, 3), round(paid_total, 3), round(full_total, 3))
                plt.figure(figsize = (12, 6))
                plt.pie((totals_arr[0], totals_arr[1]), labels = ['Deuda', 'Pagado'], colors = ['red', 'blue'], autopct = "%.2f")

                starting_text = ('Deuda Total:', 'Total Pagado:', 'Total:')
                y = 1.1
                for i, value in enumerate(totals_arr):
                    plt.text(1.2, y, f'{starting_text[i]}{value}', fontsize = '12', fontweight = 'bold', color = 'black')
                    y = y - 0.2
                plt.title(f'Deuda VS Pagado {datetime.now()}')
                plt.legend()
                plt.show()

        except(DataError, IndexError, KeyError, EmptyDataError) as e:
            print(e)




