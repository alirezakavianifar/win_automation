import time
import glob
import os.path
import pyodbc
import pandas as pd
from helpers import input_info, open_and_save_excel_files, get_update_date, time_it, log_it, check_if_col_exists, create_df, connect_to_sql
from sql_queries import create_sql_table, insert_into, insert_into_tblAnbareKoliHist, insert_into_tblAnbare99Mashaghel, insert_into_tblAnbare99Sherkatha, insert_into_tblHesabrasiArzeshAfzoode
from constants import get_sql_con, get_remote_sql_con


n_retries = 0
message_logs = ''


class DumpToSQL:
    
    def __init__(self, report_type=None, table=None, year=None, sql_delete=None, path=None, type_of_report=None):
        self.report_type = report_type
        self.table = table
        self.year = year
        self.sql_delete = sql_delete
        self.path = path
        self.type_of_report = type_of_report


                
################################################################################################################################
                
    def dump_to_sql(self):

        # Opening and saving excel files
        if self.type_of_report == 'type_one':
            open_and_save_excel_files(self.path)
            # read the csv file
            excel_files = glob.glob(os.path.join(self.path , "*.xlsx"))
        else:
            excel_files = glob.glob(os.path.join(self.path , "*.html"))

        df_values, columns = create_df(excel_files, self.year, self.report_type, self.type_of_report)
        
        if not len(df_values) == 0: 
        
            connect_to_sql(sql_query=self.sql_delete, connect_type='dropping sql table')
        
            self.sql_create_table = create_sql_table(self.table, columns)
            
            self.sql_query = insert_into(self.table, columns)
            
            # Create a new table
            connect_to_sql(self.sql_create_table, connect_type='creating sql table')
        
        # insert data into 
        
            connect_to_sql(self.sql_query, df_values=df_values, connect_type='inserting into sql table')
        
        
    def create_anbare_reports(self, year):
        sql_query = insert_into_tblAnbareKoliHist(year)
        connect_to_sql(sql_query, connect_type='inserting into sql table')
        
    def create_Anbare99Mashaghel_reports(self, year):
        sql_query = insert_into_tblAnbare99Mashaghel(year)
        connect_to_sql(sql_query, connect_type='Anbare masheghel report')
        
    def create_Anbare99Sherkatha_reports(self, year):
        sql_query = insert_into_tblAnbare99Sherkatha(year)
        connect_to_sql(sql_query, connect_type='Anbare sherkatha report')
        
        
    def create_hesabrasiArzeshAfzoode_reports(self, year):
        sql_query = insert_into_tblHesabrasiArzeshAfzoode(year)
        connect_to_sql(sql_query, connect_type='heasabrasi arzesh afzoode report')

