import numpy as np
import pandas as pd
from helpers import connect_to_sql, read_multiple_excel_sheets, get_update_date
from constants import get_sql_con, geck_location, get_remote_sql_con
import re
from sql_queries import get_sql_sanimDarjariabBadvi

column_names = {'EPD': 'عوارض آلاینده های محیط زیست',
                'INHT': 'مالیات بر ارث',
                'ITXB': 'مالیات بر درآمد مشاغل',
                'ITXC': 'مالیات بر درآمد شرکت ها',
                'RTXI': 'مالیات بر املاک برای انتقال ملک',
                'RTXR': 'مالیات بر درآمد اجاره املاک',
                'STD': 'حق تمبر',
                'VAT': 'مالیات بر ارزش افزوده',
                'WTX': 'مالیات تکلیفی',
                }
chunk_size = 1000
lst_none = ['None', 'NaT', 'nan']
saved_folder = geck_location(set_save_dir=True)
sql_conn = get_remote_sql_con()
selected_date = 140106
none_date = 999999999
selected_columns = ['نام مودی',
                    'کد ملی/شناسه ملی',
                    'کد اداره',
                    'نام اداره',
                    'سال عملکرد',
                    'منبع مالیاتی',
                    'تاریخ صدور برگ تشخیص (تاریخ تایید گزارش حسابرسی)',
                    'تاریخ ابلاغ برگ تشخیص',
                    'درآمد تشخیص',
                    'مالیات تشخیص',
                    'وضعیت ابلاغ برگ تشخیص',
                    'تاريخ ايجاد برگ قطعي',
                    'تاریخ ابلاغ برگ قطعی',
                    'مبلغ مالیات قطعی شده',
                    'وضعیت ابلاغ برگ قطعی',
                    'تاریخ بروزرسانی']

final_selected_columns = ['نام اداره',
                          'کد اداره',
                          'مالیات بر درآمد مشاغل',
                          'مالیات بر درآمد شرکت ها',
                          'مالیات بر ارزش افزوده',
                          'نام اداره سنتی',
                          'تعداد قطعی ابلاغ نشده سنیم',
                          'تاریخ بروزرسانی']
lst = []
sql_query = """
SELECT * FROM [dbo].[V_PORTAL]
"""


def get_sanim_data():
    data = connect_to_sql(sql_query,
                          sql_con=sql_conn,
                          read_from_sql=True,
                          connect_type='None',
                          return_df=True,
                          chunk_size=chunk_size)
    return data


def help_func(row, date=None, type_of=None):
    if (type_of == 't'):

        # if ((row['تاریخ ابلاغ برگ تشخیص'] in(lst_none)) & (row['تاريخ ايجاد برگ قطعي'] in (lst_none))):
        #     print('f')

        if (date is None):
            if ((row['تاریخ ابلاغ برگ تشخیص'] in (lst_none)) & (row['تاريخ ايجاد برگ قطعي'] in (lst_none))):
                return 'تشخیص ابلاغ نشده'
            else:
                return 'تشخیص ابلاغ شده'
        else:
            # if (row['کد ملی/شناسه ملی']=='14005436900'):
            #     print('f')
            if ((int(row['ماه صدور برگ تشخیص']) <= date) &
                (row['تاریخ ابلاغ برگ تشخیص'] in (lst_none)) &
                    (row['تاريخ ايجاد برگ قطعي'] in (lst_none))):
                return 'تشخیص ابلاغ نشده قبل از %s' % date

            elif ((row['تاریخ ابلاغ برگ تشخیص'] in (lst_none)) & ((row['تاريخ ايجاد برگ قطعي'] in (lst_none)))):
                return 'تشخیص ابلاغ نشده'
            else:
                return 'تشخیص ابلاغ شده'

    elif (type_of == 'g'):
        if (date is None):
            if ((row['تاریخ ابلاغ برگ قطعی'] in (lst_none)) & (row['ماه صدور برگ قطعی'] == none_date)):
                return 'قطعی صادر نشده'
            elif ((row['تاریخ ابلاغ برگ قطعی'] in (lst_none)) & (row['ماه صدور برگ قطعی'] != none_date)):
                return 'قطعی ابلاغ نشده'
            else:
                return 'قطعی ابلاغ شده'
        else:
            # if (row['کد ملی/شناسه ملی']=='14005436900'):
            #         print('f')
            if ((int(row['ماه صدور برگ قطعی']) <= date) &
                (row['ماه صدور برگ قطعی'] != none_date) &
                    (row['تاریخ ابلاغ برگ قطعی'] in (lst_none))):
                return 'قطعی ابلاغ نشده قبل از %s' % date

            elif ((row['تاریخ ابلاغ برگ قطعی'] in (lst_none)) & (row['ماه صدور برگ قطعی'] == none_date)):
                return 'قطعی صادر نشده'
            elif ((row['تاریخ ابلاغ برگ قطعی'] in (lst_none)) & (row['ماه صدور برگ قطعی'] != none_date)):
                return 'قطعی ابلاغ نشده'
            else:
                return 'قطعی ابلاغ شده'


def help_func2(row, type_of):
    if type_of == 't':
        if (row in (lst_none)):
            return none_date
        else:
            x = int(row[:6])
            return x
    elif type_of == 'g':
        if (row in (lst_none)):
            return none_date
        else:
            lst = row.split('-')
            date = get_update_date(lst)
            return int(date[:6])


def extract_num(row):
    d = re.findall(r'\d+', row)[0]
    return d


def remove_num(row):
    d = ''.join([i for i in row if not i.isdigit()])
    return "".join(d.rstrip().lstrip())


def get_tashkhis_ghatee_sanim(date=selected_date, data=get_sanim_data()):
    for i, item in enumerate(data):
        df = pd.DataFrame(item)

        df['ماه صدور برگ قطعی'] = df['تاريخ ايجاد برگ قطعي'].str.replace(
            '/', '')
        df['ماه صدور برگ قطعی'] = df['ماه صدور برگ قطعی'].apply(
            lambda x: help_func2(x, type_of='t'))
        df['ماه ابلاغ برگ قطعی'] = df['تاریخ ابلاغ برگ قطعی'].str.slice(0, 10)
        df['ماه ابلاغ برگ قطعی'] = df['ماه ابلاغ برگ قطعی'].apply(
            lambda x: help_func2(x, type_of='g'))
        df['وضعیت ابلاغ برگ قطعی'] = df.apply(
            lambda row: help_func(row, selected_date, type_of='g'), axis=1)

        df['ماه صدور برگ تشخیص'] = df['تاریخ صدور برگ تشخیص (تاریخ تایید گزارش حسابرسی)'].str.replace(
            '/', '')
        df['ماه صدور برگ تشخیص'] = df['ماه صدور برگ تشخیص'].apply(
            lambda x: help_func2(x, type_of='t'))
        df['ماه ابلاغ برگ تشخیص'] = df['تاریخ ابلاغ برگ تشخیص'].str.replace(
            '/', '')
        df['ماه ابلاغ برگ تشخیص'] = df['ماه ابلاغ برگ تشخیص'].apply(
            lambda x: help_func2(x, type_of='t'))
        df['وضعیت ابلاغ برگ تشخیص'] = df.apply(
            lambda row: help_func(row, selected_date, type_of='t'), axis=1)

        if not (df.empty):
            lst.append(df)
        print(i)
        # if i == 6:
        #     break

    final_df = pd.concat(lst)
    final_df = final_df[selected_columns]

    if not (final_df.empty):
        g_by_eblagh = final_df.groupby(['وضعیت ابلاغ برگ قطعی'])
        t_by_eblagh = final_df.groupby(['وضعیت ابلاغ برگ تشخیص'])

        lst_t = []
        lst_g = []
        for g_type, df_g in g_by_eblagh:
            if (g_type == 'قطعی ابلاغ نشده قبل از %s' % selected_date):
                dff = g_by_eblagh.get_group(g_type)
                lst_g.append(dff)

        for t_type, df_t in t_by_eblagh:
            if (t_type == 'تشخیص ابلاغ نشده قبل از %s' % selected_date):
                dff = t_by_eblagh.get_group(t_type)
                lst_t.append(dff)

        if not lst_t:
            print('list is empty')
        else:

            dff_t = pd.concat(lst_t)
            dff_agg_t = dff_t.groupby(
                ['کد اداره', 'نام اداره', 'منبع مالیاتی']).size().reset_index()
            dff_agg_t = pd.pivot_table(dff_agg_t, values=['کد اداره'], index=['نام اداره', 'کد اداره'],
                                       columns=['منبع مالیاتی'], aggfunc=np.sum, fill_value=0).reset_index()
            dff_agg_t.columns = dff_agg_t.columns.get_level_values(1)

            dff_agg_t.rename(columns=column_names, inplace=True)
            dff_agg_t.columns.values[0] = 'نام اداره'
            dff_agg_t.columns.values[1] = 'کد اداره'
            # dff_agg_t['نام اداره سنتی'] = dff_agg_t['نام اداره'].apply(lambda x: extract_num(x))
            dff_agg_t.to_excel('%s/no-eblagh_t_agg.xlsx' % saved_folder)
            dff_t.to_excel('%s/no-eblagh_t.xlsx' % saved_folder)

        if not lst_g:
            print('list is empty')
        else:

            dff_g = pd.concat(lst_g)
            dff_agg_g = dff_g.groupby(
                ['کد اداره', 'نام اداره']).size().reset_index()
            dff_agg_g.rename(
                columns={0: 'تعداد قطعی ابلاغ نشده سنیم'}, inplace=True)
            dff_agg_g.to_excel('%s/no-eblagh_g_agg.xlsx' % saved_folder)
            dff_g.to_excel('%s/no-eblagh_g.xlsx' % saved_folder)

        dff_agg_merged = pd.merge(dff_agg_t, dff_agg_g, left_on='کد اداره',
                                  right_on='کد اداره', how='outer', suffixes=('', '_y'), indicator=True)
        dff_agg_merged['نام اداره'].fillna(
            dff_agg_merged['نام اداره_y'], inplace=True)
        dff_agg_merged['نام اداره_y'].fillna(
            dff_agg_merged['نام اداره'], inplace=True)
        dff_agg_merged.drop(columns=['نام اداره_y', '_merge'], inplace=True)
        new_col = dff_agg_merged['نام اداره'].apply(lambda x: extract_num(x))
        dff_agg_merged.insert(1, 'نام اداره سنتی', new_col)
        new_col = dff_agg_merged['نام اداره'].apply(lambda x: remove_num(x))
        dff_agg_merged.insert(0, 'شهرستان', new_col)
        dff_agg_merged.fillna(0, inplace=True)
        dff_agg_merged.drop(dff_agg_merged.filter(
            regex='_y$').columns, axis=1, inplace=True)
        del dff_agg_merged['نام اداره']
        dff_agg_merged['تاریخ بروزرسانی'] = get_update_date()

        # dff_agg_merged.rename(columns=final_selected_columns, inplace=True)
        # dff_agg_t['نام اداره سنتی'] = df['نام اداره'].apply(lambda x: extract_num(x))
        dff_agg_merged.to_excel('%s/no-eblagh_merged.xlsx' % saved_folder)
        dff_agg_merged = dff_agg_merged[['شهرستان', 'نام اداره سنتی', 'کد اداره', 'مالیات بر درآمد مشاغل',
                                         'مالیات بر درآمد شرکت ها', 'مالیات بر ارزش افزوده', 'تعداد قطعی ابلاغ نشده سنیم', 'تاریخ بروزرسانی']]
        return lst_t, lst_g, dff_agg_merged


def get_badvi_sanim():

    sql_query = get_sql_sanimDarjariabBadvi()
    df_badviSanim = connect_to_sql(
        sql_query, read_from_sql=True, connect_type='', return_df=True)

    dff_agg_b = df_badviSanim.groupby(
        ['نام اداره']).size().reset_index()
    new_col = dff_agg_b['نام اداره'].apply(lambda x: extract_num(x))
    dff_agg_b.insert(1, 'نام اداره سنتی', new_col)
    new_col = dff_agg_b['نام اداره'].apply(lambda x: remove_num(x))
    dff_agg_b.insert(0, 'شهرستان', new_col)
    dff_agg_b.drop('نام اداره', axis=1, inplace=True)
    dff_agg_b.rename(
        columns={0: 'تعداد آماده ارسال به هیات سنیم'}, inplace=True)

    return df_badviSanim, dff_agg_b
