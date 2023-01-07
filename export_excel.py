
from pymysql import*
import pandas.io.sql as sql

# connect the mysql with the python

def export_to_excel(address, name):
    con = connect(
        host="localhost",
        user="root",
        passwd="Bismillah")

    # read the data
    df = sql.read_sql('SELECT book_name, amount, sale_price, total_price,'
                    'salesman, date_time FROM Library.days_record_for_sale', con)

    df1 = sql.read_sql('SELECT total_price FROM Library.days_record_for_sale', con)

    # print the data
    print(len(df))
    df1 = df1["total_price"].sum()
    print(df1)

    df['total_sale_amount'] = df1
    # export the data into the excel sheet
    # df.to_excel('ds3.xls', index=False)

    df.to_excel(rf'{address}/{name}.xls', index=False)