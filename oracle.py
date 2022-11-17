import os
import cx_Oracle
import pandas as pd
from helpers import connect_to_sql, get_update_date
from sql_queries import sql_delete, create_sql_table, insert_into, get_sql_allsanim, \
    get_sql_sanimusers, get_sql_allhesabrasi, get_sql_alleterazat, get_sql_allbakhshodegi, get_sql_allhesabdari, get_sql_allanbare
import time


base_path = r'C:\Users\alkav\Desktop\final_scripts\mappingSanim'
excel_files = {'allsanim': 'allsanim.xlsx',
               'allusers': 'allusers.xlsx',
               'allhesabrasi': 'allhesabrasi.xlsx',
               'alleterazat': 'alleterazat.xlsx',
               'allbakhshodegi': 'allbakhshodegi.xlsx',
               'allhesabdari': 'allhesabdari.xlsx',
               'allanbare': 'allanbare.xlsx'}

tbl_names = {'allsanim': 'V_PORTAL',
             'allusers': 'V_USERS',
             'allhesabrasi': 'V_AUD35',
             'alleterazat': 'V_OBJ60',
             'allbakhshodegi': 'V_IMPUNITY',
             'allhesabdari': 'V_EHMOADI',
             'allanbare': 'V_AUDPOOL'}

cx_Oracle.init_oracle_client(lib_dir=r"E:\downloads\instantclient_21_7")

# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.


def get_allSanim(excel_file, selected_sql_query, tbl_name):
    connection = cx_Oracle.connect(user="ostan_khozestan", password="S_KfvDKu_9851z@hFsTf",
                                   dsn="10.1.1.200:1521/EXTDB")
    path = os.path.join(base_path, excel_file)
    cursor = connection.cursor()
    cursor.execute(selected_sql_query)
    # Get the name of columns
    columns = cursor.description
    cols_lst = []

    for c in columns:
        cols_lst.append(c[0])

    df_cols_lst = pd.DataFrame(cols_lst, columns=['engcol'])
    df_mapping = pd.read_excel(path)

    df_final_mapping = df_cols_lst.merge(
        df_mapping, how='left', left_on='engcol', right_on='engcol')
    df_final_mapping['percol'] = df_final_mapping['percol'].combine_first(
        df_cols_lst['engcol'])

    column_names = df_final_mapping['percol']
    column_date = pd.Series(['تاریخ بروزرسانی'])
    column_names = column_names.append(column_date, ignore_index=True)

    sql_delete_query = sql_delete(tbl_name)
    connect_to_sql(sql_query=sql_delete_query,
                   connect_type='dropping sql table')

    sql_create_table_query = create_sql_table(tbl_name, column_names)
    connect_to_sql(sql_create_table_query, connect_type='creating sql table')

    # Fetch data
    num_rows = 200000
    while True:
        rows = cursor.fetchmany(num_rows)
        if not rows:
            break
        # Create a dataframe with column names
        df = pd.DataFrame(rows, columns=column_names[:-1])
        df['تاریخ بروزرسانی'] = get_update_date()
        df = df.astype(str)
        sql_insert = insert_into(tbl_name, column_names)
        connect_to_sql(sql_query=sql_insert, df_values=df.values.tolist(
        ), connect_type='inserting into sql table')

    cursor.close()
    connection.close()


if __name__ == '__main__':

    get_allSanim(excel_files['allsanim'], selected_sql_query=get_sql_allsanim(
    ), tbl_name=tbl_names['allsanim'])

    get_allSanim(excel_files['allusers'], selected_sql_query=get_sql_sanimusers(
    ), tbl_name=tbl_names['allusers'])

    get_allSanim(excel_files['alleterazat'], selected_sql_query=get_sql_alleterazat(
    ), tbl_name=tbl_names['alleterazat'])

    get_allSanim(excel_files['allbakhshodegi'], selected_sql_query=get_sql_allbakhshodegi(
    ), tbl_name=tbl_names['allbakhshodegi'])

    get_allSanim(excel_files['allhesabdari'], selected_sql_query=get_sql_allhesabdari(
    ), tbl_name=tbl_names['allhesabdari'])

    get_allSanim(excel_files['allanbare'], selected_sql_query=get_sql_allanbare(
    ), tbl_name=tbl_names['allanbare'])

    get_allSanim(excel_files['allhesabrasi'], selected_sql_query=get_sql_allhesabrasi(
    ), tbl_name=tbl_names['allhesabrasi'])
