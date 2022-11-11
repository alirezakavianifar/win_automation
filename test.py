from helpers import read_multiple_excel_sheets
import pandas as pd

df = df=read_multiple_excel_sheets(r'D:\PN721.AllTaxpayers.16.xls')

df_1 = df[['نام شرکت/نام واحدصنفی','آدرس', 'مودی اصلی/ مدیرعامل', 'شماره همراه','شهرستان']]

df_1_filtered = df_1.loc[df_1['نام شرکت/نام واحدصنفی'].str.contains('مهد کودک', na=False)]
df_1_filtered_1 = df_1.loc[df_1['نام شرکت/نام واحدصنفی'].str.contains('مهدکودک', na=False)]

df_1_filtered_1 = df_1_filtered_1.loc[df_1_filtered_1['شهرستان']=='اهواز']

ddd = pd.concat([df_1_filtered, df_1_filtered_1])

ddd = ddd.drop_duplicates()

ddd.to_excel(r'H:\automating_reports\monthly_reports\saved_dir\mahd.xlsx')