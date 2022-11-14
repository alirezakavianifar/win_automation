from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import glob
import numpy as np
import os.path
import pandas as pd
from datetime import datetime
import argparse
import jdatetime
import xlwings as xw
import shutil
import pandas as pd
import openpyxl
import datetime as dt
from datetime import datetime
from functools import wraps
import functools as ft
import math
from tqdm import tqdm
import pyodbc
from constants import geck_location, set_gecko_prefs, get_remote_sql_con, get_sql_con, get_str_help, get_comm_reports, get_heiat, get_lst_reports, \
    get_all_years, get_common_years, get_str_years, get_years, get_common_reports, get_comm_years, get_heiat_reports, get_server_namesV2
from sql_queries import get_sql_mashaghelsonati, get_sql_mashaghelsonati_ghatee, get_sql_mashaghelsonati_tashkhisEblaghNoGhatee, \
    get_sql_mashaghelsonati_ghateeEblaghNashode, get_sql_mashaghelsonati_tashkhisEblaghNashode, \
    get_sql_mashaghelsonati_amadeersalbeheiat, \
    sql_delete, create_sql_table, insert_into


n_retries = 0
year = 0
report_type = 0


log_folder_name = 'C:\ezhar-temp'
log_excel_name = 'excel.xlsx'
log_dir = os.path.join(log_folder_name, log_excel_name)
saved_folder = geck_location(set_save_dir=False)


def retry(func):
    def try_it():
        global n_retries
        try:
            result = func()
            return result

        except Exception as e:
            n_retries += 1
            print(e)
            if n_retries < 5:
                try_it()

    return try_it


def retry_with_arguments(driver=None):
    def retry(func):
        def try_it(*args, **kwargs):
            global n_retries
            try:
                result = func(*args, **kwargs)
                return result

            except Exception as e:
                print('error occured. please pay close attention')
                n_retries += 1
                # print(e)
                if n_retries < 5:
                    driver.close()
                    time.sleep(4)
                    try_it()

        return try_it
    return retry


def maybe_make_dir(directory):
    for item in directory:

        if not os.path.exists(item):
            os.makedirs(item)


def read_multiple_excel_sheets(path):
    df = pd.read_excel(path, sheet_name=None)
    list = []

    for key in df:
        list.append(df[key])

    df = pd.concat(list)

    return df


def remove_excel_files(files=None, pathsave=None):
    for f in files:

        if os.path.exists(f):

            os.remove(f)


def merge_multiple_excel_sheets(path, dest, return_df=False, delete_after_merge=False, postfix='.xls', db_save=False, table=None):
    lst = []
    file_list = glob.glob(path + "/*" + postfix)

    for item in file_list:
        df = pd.read_excel(item, sheet_name=None)

        for key, value in df.items():
            lst.append(value)
        if delete_after_merge:
            remove_excel_files([item])

    df_all = pd.concat(lst)
    df_all_columns = df_all.columns.tolist()
    df_values = df_all.values.tolist()
    dest = os.path.join(dest, 'codeeghtesadi.csv')

    df_all = pd.read_excel(
        r'E:\automating_reports_V2\saved_dir\codeghtesadi\codeeghtesadi.xlsx')

    df_all.to_csv(dest)

    if db_save:
        drop_into_db(table_name=table, columns=df_all.columns.tolist(),
                     values=df_all.values.tolist())

    if return_df:
        return df_all
    else:
        del df_all


def rename_files(path, dest, prefix='.xls', postfix='.html'):
    file_list = glob.glob(path + "/*" + prefix)

    for i, item in enumerate(file_list):

        dest1 = os.path.join(dest, '%s%s' % (i, postfix))
        os.rename(item, dest1)


def merge_multiple_html_files(path, return_df=False, delete_after_merge=True):
    file_list = glob.glob(path + "/*.html")

    merge_excels = []
    for item in file_list:
        # df = pd.read_html(item, flavor="html5lib")[0]
        df = pd.read_html(item)[0]
        merge_excels.append(df)

    final_df = pd.concat(merge_excels)

    path = os.path.join(path, 'final_df.csv')
    if delete_after_merge:
        remove_excel_files(files=file_list)
    final_df.to_csv(path)

    if return_df:
        return final_df
    else:
        del final_df


def merge_multiple_excel_files(path, dest, excel_name='merged', table_name='default',
                               delete_after_merge=True, return_df=False,
                               postfix='xlsx', postfix_after_merge='xlsx', drop_to_sql=False, append_to_prev=False):

    # dest = dest + '/' + str(excel_name) + postfix
    dest = os.path.join(dest, excel_name)
    maybe_make_dir([dest])
    dest = os.path.join(dest, table_name +
                        '.' + postfix_after_merge)

    # csv files in the path
    file_list = glob.glob(path + "/*.%s" % postfix)

    excel_files = glob.glob(os.path.join(path, "*.%s" % postfix))
    merge_excels = []

    for f in excel_files:
        try:
            df = pd.read_excel(f)
            merge_excels.append(df)
        except Exception as e:
            save_excel(f, log=False)
            df = pd.read_excel(f)
            merge_excels.append(df)

    # Merge all dataframes into one
    final_df_all_fine_grained = pd.concat(merge_excels)
    final_df_all_fine_grained = final_df_all_fine_grained.astype('str')
    final_df_all_fine_grained['تاریخ بروزرسانی'] = get_update_date()

    if delete_after_merge:
        remove_excel_files(files=file_list)

    if drop_to_sql:

        drop_into_db(table_name=table_name,
                     columns=final_df_all_fine_grained.columns.tolist(),
                     values=final_df_all_fine_grained.values.tolist(),
                     append_to_prev=append_to_prev)

    final_df_all_fine_grained.to_excel(dest, index=False)

    print('merging was done successfully')
    if return_df:
        return final_df_all_fine_grained

    else:
        del final_df_all_fine_grained


@retry
def input_info():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reportTypes', type=str, help=get_str_help())
    parser.add_argument('--years', type=str, help=get_str_years())
    parser.add_argument('--s',  type=str, nargs='?',
                        default='not-s', help='types:\nt = True\nf = False\n')
    parser.add_argument('--d',  type=str, nargs='?',
                        default='not-d', help='types:\nt = True\nf = False\n')
    parser.add_argument('--c',  type=str, nargs='?',
                        default='not-c', help='types:\nt = True\nf = False\n')
    args = parser.parse_args()

    selected_report_types = args.reportTypes.split(',')  # ['1','2','3','4']
    selected_years = args.years.split(',')
    all_years = get_all_years()
    comm_reports = get_comm_reports()
    comm_years = get_comm_years()
    heiat = get_heiat()
    dump_to_sql = args.d
    create_reports = args.c
    scrape = args.s

    new_reportTypes = []
    new_years = []
    report_types = get_lst_reports()
    years = get_years()
    common_reports = get_common_reports()
    common_years = get_common_years()
    heiat_reports = get_heiat_reports()

    if selected_report_types.count(comm_reports):
        for report_type in common_reports:
            new_reportTypes.append(report_type)

    elif selected_report_types.count(heiat):
        for report_type in heiat_reports:
            new_reportTypes.append(report_type[0])

    else:

        for report_type in report_types:
            if (selected_report_types.count(report_type[1])):
                new_reportTypes.append(report_type[0])

    if selected_years.count(all_years):

        for year in years:
            new_years.append(year[0])

    elif selected_years.count(comm_years):
        for year in common_years:
            new_years.append(year[0])

    else:

        for year in years:
            if (selected_years.count(year[1])):
                new_years.append(year[0])

    return new_reportTypes, new_years, scrape, dump_to_sql, create_reports


def get_update_date(date=None):
    if date is None:
        x = jdatetime.date.today()
        if len(str(x.month)) == 1:
            month = '0%s' % str(x.month)
        else:
            month = str(x.month)
        if len(str(x.day)) == 1:
            day = '0%s' % str(x.day)

        else:
            day = str(x.day)

        year = str(x.year)

    else:
        gdate = jdatetime.GregorianToJalali(
            int(date[0]), int(date[1]), int(date[2]))
        year = str(gdate.jyear)
        month = str(gdate.jmonth)
        day = str(gdate.jday)

        if len(str(month)) == 1:
            month = '0%s' % str(month)
        else:
            month = str(month)
        if len(str(day)) == 1:
            day = '0%s' % str(day)

        else:
            day = str(day)

    update_date = year + month + day

    return update_date


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('The operation %s was done successfully' %
              kwargs['connect_type'])
        print(func.__name__ + ' took ' + str((end - start)) + ' seconds')
        return result
    return wrapper


def make_dir_if_not_exists(paths):
    for path in paths:
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(path)


def check_if_up_to_date(func):
    @wraps(func)
    def try_it(*args, **kwargs):
        if kwargs['log'] == False:
            result = func(*args, **kwargs)
            return result
        current_date = int(get_update_date())
        func_name = func.__name__
        if func_name == 'is_updated_to_save':
            type_of = 'save_excel'
        elif func_name == 'is_updated_to_download':
            type_of = 'download_excel'
        else:
            type_of = 'save_excel'

        df = pd.read_excel(log_dir)
        check_date = df['date'].where(
            (df['file_name'] == args[0]) & (df['type_of'] == type_of)).max()

        if not math.isnan(check_date):

            if (int(check_date) == int(current_date) and func_name != 'save_excel'):
                print('The %s have already been logged' % args[0])
                result = func(*args, **kwargs)
                return result

            elif (int(check_date) != int(current_date) and func_name == 'save_excel'):
                print('opening excel')
                result = func(*args, **kwargs)
                return result
            else:
                return False

        elif (math.isnan(check_date) and func_name == 'is_updated_to_save'):
            return False

        elif (math.isnan(check_date) and func_name == 'is_updated_to_download'):
            return False

        else:

            result = func(*args, **kwargs)
            return result

            # return print('The file %s has already been updated \n' % args[0])

    return try_it


def log_it(func):

    @wraps(func)
    def try_it(*args, **kwargs):
        if kwargs['log'] == False:
            result = func(*args, **kwargs)
            return result
        print('log_it initialized')
        d1 = datetime.now()
        type_of = func.__name__

        if (func.__name__ == 'save_excel'):

            print('opening %s for saving' % args[0])

        result = func(*args, **kwargs)

        c_date = get_update_date()

        if type_of == 'download_excel':

            df_1 = pd.DataFrame([[result, c_date, type_of]], columns=[
                                'file_name', 'date', 'type_of'])

        else:

            df_1 = pd.DataFrame([[args[0], c_date, type_of]], columns=[
                                'file_name', 'date', 'type_of'])

        # create excel file for logging if it does not already exist
        if not os.path.exists(log_dir):

            df_1.to_excel(log_dir)

        else:

            df_2 = pd.read_excel(log_dir, index_col=0)

            df_3 = pd.concat([df_1, df_2])

            remove_excel_files([log_dir])

            df_3.to_excel(log_dir)

        d2 = datetime.now()
        d3 = (d2 - d1).total_seconds() / 60

        if type_of == 'download_excel':

            print('it took %s minutes for the %s to be logged' %
                  ("%.2f" % d3, kwargs['type_of_excel']))

        else:

            print('it took %s minutes for the %s to be logged' %
                  ("%.2f" % d3, args[0]))

        print('***********************************************************************\n')

        return result

    return try_it


@check_if_up_to_date
def is_updated_to_save(path):
    return True


@check_if_up_to_date
@log_it
def save_excel(excel_file, log=True):
    irismash = xw.Book(excel_file)
    irismash.save()
    irismash.app.quit()
    time.sleep(8)


def open_and_save_excel_files(path, report_type=None, year=None, merge=False):

    excel_files = glob.glob(os.path.join(path, "*.xlsx"))

    for f in excel_files:
        save_excel(f)


@check_if_up_to_date
def is_updated_to_download(path):
    return True


@check_if_up_to_date
def is_updated_to_save(path):
    return True


def check_if_col_exists(df, col):
    if col in df:
        return True
    else:
        return False


def init_driver(pathsave, driver_type='firefox'):
    if driver_type == 'chrome':
        options = Options()
        prefs = {'download.default_directory': pathsave}
        options.add_argument("start-maximized")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option(
            "prefs", {"download.default_directory": pathsave})

        # s = Service('C:\\BrowserDrivers\\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=geck_location(
            driver_type='chrome'), options=options)

    else:

        fp = webdriver.FirefoxProfile()
        fp.set_preference('browser.download.folderList', 2)
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.dir', pathsave)

        fp.set_preference('browser.helperApps.neverAsk.openFile',
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream')
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream;application/excel')
        fp.set_preference('browser.helperApps.alwaysAsk.force', False)
        fp.set_preference('browser.download.manager.alertOnEXEOpen', False)
        fp.set_preference('browser.download.manager.focusWhenStarting', False)
        fp.set_preference('browser.download.manager.useWindow', False)
        fp.set_preference(
            'browser.download.manager.showAlertOnComplete', False)
        fp.set_preference('browser.download.manager.closeWhenDone', False)

        driver = webdriver.Firefox(fp, executable_path=geck_location())
        driver.window_handles
        driver.switch_to.window(driver.window_handles[0])

    return driver


def create_df(excel_files, year=None, report_type=None, type_of_report=None):

    merge_excels = []
    # Convert excel files into dataframes
    for f in excel_files:

        if f == r'C:\ezhar-temp\%s\%s\Excel.xlsx' % (year, report_type):
            df = pd.read_excel(f)

            if (check_if_col_exists(df, "منبع مالیاتی") == False):
                df.insert(11, column='منبع مالیاتی',
                          value='مالیات بر درآمد شرکت ها')
            merge_excels.append(df)

        if f == r'C:\ezhar-temp\%s\%s\Excel(1).xlsx' % (year, report_type):
            df = pd.read_excel(f)
            if (check_if_col_exists(df, "منبع مالیاتی") == False):
                df.insert(11, column='منبع مالیاتی',
                          value='مالیات بر درآمد مشاغل')
            merge_excels.append(df)

        if f == r'C:\ezhar-temp\%s\%s\Excel(2).xlsx' % (year, report_type):
            df = pd.read_excel(f)
            if (check_if_col_exists(df, "منبع مالیاتی") == False):
                df.insert(11, column='منبع مالیاتی',
                          value='مالیات بر ارزش افزوده')
            merge_excels.append(df)

        if f == r'C:\ezhar-temp\%s\%s\جزئیات اعتراضات و شکایات.html' % (year, report_type):

            df = pd.read_html(f, flavor="html5lib")[0]
            merge_excels.append(df)

    # Merge all dataframes into one
    final_df_all_fine_grained = pd.concat(merge_excels)

    # Clean the Dataframe
    final_df_all_fine_grained = final_df_all_fine_grained.fillna(value=0)
    final_df_all_fine_grained['تاریخ بروزرسانی'] = get_update_date()

    if (check_if_col_exists(final_df_all_fine_grained, "شناسه ملی / کد ملی (TIN)")):
        final_df_all_fine_grained['شناسه ملی / کد ملی (TIN)'] = final_df_all_fine_grained['شناسه ملی / کد ملی (TIN)'].astype(
            str)

    final_df_all_fine_grained['شناسه اظهارنامه'] = final_df_all_fine_grained['شناسه اظهارنامه'].astype(
        str)

    if (check_if_col_exists(final_df_all_fine_grained, "سال عملکرد") == False):
        final_df_all_fine_grained.insert(2, column='سال عملکرد', value=year)

    if (check_if_col_exists(final_df_all_fine_grained, "کد پستی مودی") == False):
        final_df_all_fine_grained.insert(
            6, column='کد پستی مودی', value='none')

    if (check_if_col_exists(final_df_all_fine_grained, "نوع ریسک اظهارنامه") == False):
        final_df_all_fine_grained.insert(
            21, column='نوع ریسک اظهارنامه', value='none')

    if (check_if_col_exists(final_df_all_fine_grained, "مالیات تشخیص")):
        final_df_all_fine_grained['مالیات تشخیص'] = final_df_all_fine_grained['مالیات تشخیص'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "مالیات تشخیصی")):
        final_df_all_fine_grained['مالیات تشخیصی'] = final_df_all_fine_grained['مالیات تشخیصی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "مالیات قطعی")):
        final_df_all_fine_grained['مالیات قطعی'] = final_df_all_fine_grained['مالیات قطعی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "برگ مطالبه جرایم موضوع ماده 169 ق.م.م")):
        final_df_all_fine_grained['برگ مطالبه جرایم موضوع ماده 169 ق.م.م'] = final_df_all_fine_grained['برگ مطالبه جرایم موضوع ماده 169 ق.م.م'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "کد رهگیری ثبت نام")):
        final_df_all_fine_grained['کد رهگیری ثبت نام'] = final_df_all_fine_grained['کد رهگیری ثبت نام'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "مالیات ابرازی")):
        final_df_all_fine_grained['مالیات ابرازی'] = final_df_all_fine_grained['مالیات ابرازی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "درآمد ابرازی")):
        final_df_all_fine_grained['درآمد ابرازی'] = final_df_all_fine_grained['درآمد ابرازی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "شماره برگ قطعی")):
        final_df_all_fine_grained['شماره برگ قطعی'] = final_df_all_fine_grained['شماره برگ قطعی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "درآمد تشخیصی")):
        final_df_all_fine_grained['درآمد تشخیصی'] = final_df_all_fine_grained['درآمد تشخیصی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "مالیات اعتراض")):
        final_df_all_fine_grained['مالیات اعتراض'] = final_df_all_fine_grained['مالیات اعتراض'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "درآمد بدوی")):
        final_df_all_fine_grained['درآمد بدوی'] = final_df_all_fine_grained['درآمد بدوی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "مالیات بدوی")):
        final_df_all_fine_grained['مالیات بدوی'] = final_df_all_fine_grained['مالیات بدوی'].astype(
            np.int64)

    if (check_if_col_exists(final_df_all_fine_grained, "درآمد اعتراض")):
        final_df_all_fine_grained['درآمد اعتراض'] = final_df_all_fine_grained['درآمد اعتراض'].astype(
            np.int64)
    if (report_type == 'ezhar'):
        final_df_all_fine_grained['عوارض ابرازی'] = final_df_all_fine_grained['عوارض ابرازی'].astype(
            np.int64)
        final_df_all_fine_grained['کد رهگیری اظهارنامه'] = final_df_all_fine_grained['کد رهگیری اظهارنامه'].astype(
            str)
        final_df_all_fine_grained['فروش ابرازی'] = final_df_all_fine_grained['فروش ابرازی'].astype(
            np.int64)
        final_df_all_fine_grained['اعتبار ابرازی'] = final_df_all_fine_grained['اعتبار ابرازی'].astype(
            np.int64)

    elif (report_type == 'tashkhis_sader_shode' or report_type == 'tashkhis_eblagh_shode' or report_type == 'ghatee_sader_shode' or report_type == 'ghatee_eblagh_shode'):

        if (check_if_col_exists(final_df_all_fine_grained, "کد ملی حسابرس اصلی")):
            final_df_all_fine_grained['کد ملی حسابرس اصلی'] = final_df_all_fine_grained['کد ملی حسابرس اصلی'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "شماره برگه تشخیص")):
            final_df_all_fine_grained['شماره برگه تشخیص'] = final_df_all_fine_grained['شماره برگه تشخیص'].astype(
                str)

        if (check_if_col_exists(final_df_all_fine_grained, "مالیات تشخیص")):
            final_df_all_fine_grained['مالیات تشخیص'] = final_df_all_fine_grained['مالیات تشخیص'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "فروش تشخیص")):
            final_df_all_fine_grained['فروش تشخیص'] = final_df_all_fine_grained['فروش تشخیص'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "درآمد تشخیص")):
            final_df_all_fine_grained['درآمد تشخیص'] = final_df_all_fine_grained['درآمد تشخیص'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "عوارض تشخیص")):
            final_df_all_fine_grained['عوارض تشخیص'] = final_df_all_fine_grained['عوارض تشخیص'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "درآمد قطعی")):
            final_df_all_fine_grained['درآمد قطعی'] = final_df_all_fine_grained['درآمد قطعی'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "عوارض قطعی")):
            final_df_all_fine_grained['عوارض قطعی'] = final_df_all_fine_grained['عوارض قطعی'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "اعتبار قطعی")):
            final_df_all_fine_grained['اعتبار قطعی'] = final_df_all_fine_grained['اعتبار قطعی'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "پرداخت")):
            final_df_all_fine_grained['پرداخت'] = final_df_all_fine_grained['پرداخت'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "مانده بدهی")):
            final_df_all_fine_grained['مانده بدهی'] = final_df_all_fine_grained['مانده بدهی'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "شماره برگ تشخیص")):
            final_df_all_fine_grained['شماره برگ تشخیص'] = final_df_all_fine_grained['شماره برگ تشخیص'].astype(
                np.int64)

        if (check_if_col_exists(final_df_all_fine_grained, "مالیات")):
            final_df_all_fine_grained['مالیات'] = final_df_all_fine_grained['مالیات'].astype(
                np.int64)

    return final_df_all_fine_grained.values.tolist(), final_df_all_fine_grained.columns


@time_it
def connect_to_sql(sql_query, sql_con=get_sql_con(), df_values=None, read_from_sql=False, connect_type=None, return_df=False, chunk_size=None):

    global n_retries

    def retry():

        cnxn = pyodbc.connect(
            sql_con)
        cursor = cnxn.cursor()

        if (read_from_sql):
            df = pd.read_sql(sql_query, cnxn, chunksize=chunk_size)
            return df

        if df_values == None:
            cursor.execute(sql_query)
            cursor
            cursor.execute('commit')
        else:
            cursor.executemany(sql_query, df_values)
            cursor.execute('commit')
        cnxn.close()

    try:
        if return_df:
            x = retry()
            return x
        else:
            retry()

    except Exception as e:
        if n_retries < 6:
            n_retries += 1
            print(e)
            time.sleep(3)
            print('trying again')
            time.sleep(4)
            retry()


class Login:
    def __init__(self, pathsave):
        self.pathsave = pathsave
        fp = set_gecko_prefs(pathsave)
        self.driver = webdriver.Firefox(fp, executable_path=geck_location())
        self.driver.window_handles
        self.driver.switch_to.window(self.driver.window_handles[0])

    def __call__(self):
        return self.driver

    def close(self):
        self.driver.close()


def login_tgju(driver):
    driver.get("https://www.tgju.org/")
    driver.implicitly_wait(20)
    
    return driver
    

def login_arzeshafzoodeh(driver):
    driver.get("http://10.2.16.131/frmManagerLogin2.aspx")
    driver.implicitly_wait(20)
    txtUserName = driver.find_element(
        By.NAME, 'txtusername').send_keys('959396')
    txtPassword = driver.find_element(
        By.NAME, 'txtpassword').send_keys('62253LBG')
    time.sleep(10)
    driver.find_element(By.NAME, 'btnlogin').click()

    return driver


def login_codeghtesadi(driver):
    driver.get("http://management.tax.gov.ir/Public/Login")
    driver.implicitly_wait(5)
    txtUserName = driver.find_element(
        By.ID, 'username').send_keys('1756914443')
    txtPassword = driver.find_element(
        By.ID, 'Password').send_keys('1756914443')
    time.sleep(10)
    driver.find_element(By.CLASS_NAME, 'button').click()
    time.sleep(1)

    return driver


def login_mostaghelat(driver):
    driver.get("http://most.tax.gov.ir/")
    driver.implicitly_wait(20)
    txtUserName = driver.find_element(
        By.NAME, 'Txt_username').send_keys('1930841086')
    txtPassword = driver.find_element(
        By.NAME, 'Txt_Password').send_keys('193084193084')
    time.sleep(0.5)
    driver.find_element(By.NAME, 'login_btn').click()

    return driver


def login_sanim(driver):
    driver.get("https://mgmt.tax.gov.ir/ords/f?p=100:101:16540338045165:::::")
    driver.implicitly_wait(20)
    txtUserName = driver.find_element_by_id(
        'P101_USERNAME').send_keys('1971385018')
    txtPassword = driver.find_element_by_id(
        'P101_PASSWORD').send_keys('123456')

    driver.find_element(By.ID, 'B1700889564218640').click()

    return driver


def get_tblreports_date(tblnames, years=['1395', '1396', '1397', '1398', '1399']):

    lst = []

    for year in years:

        for tblname in tblnames:

            sql_query = """
            
            select distinct [تاریخ بروزرسانی] from [dbo].[%s%s] 
            
            """ % (tblname, year)

            date = connect_to_sql(sql_query, sql_con=get_sql_con(
                server='10.52.0.114'), read_from_sql=True, connect_type='', return_df=True)

            if not (date.empty):
                date = date.values.tolist()
                lst.append((tblname, year, date[0][0]))

    return lst


def get_mashaghelsonati(mashaghel_type, date=None, eblagh=True, save_on_folder=False, saved_folder=saved_folder, save_how='db'):

    i = 0
    j = 24

# Specify sql query
    if (mashaghel_type == "tashkhis" and eblagh == False):
        sql_query = get_sql_mashaghelsonati_tashkhisEblaghNashode()
    elif (mashaghel_type == "ghatee" and eblagh == False):
        sql_query = get_sql_mashaghelsonati_ghateeEblaghNashode()
    elif mashaghel_type == "tashkhis":
        # sql_query = get_sql_mashaghelsonati()
        sql_query = get_sql_mashaghelsonati_tashkhisEblaghNoGhatee()
    elif mashaghel_type == "heiat":
        sql_query = get_sql_mashaghelsonati_amadeersalbeheiat(date=date)
    elif mashaghel_type == "ghatee":
        sql_query = get_sql_mashaghelsonati_ghatee()

    # Go through each server one by one
    servers = get_server_namesV2()
    all_df = []

    for i, server in tqdm(enumerate(servers[i:j])):
        df = connect_to_sql(sql_query, sql_con=get_sql_con(
            server=servers[i][1], database='MASHAGHEL', username='mash', password='123456'), read_from_sql=True, connect_type='',  return_df=True)
        all_df.append(df)
        i += 1
    # merge all dfs
    df_all = pd.concat(all_df)
    df_all['تاریخ بروزرسانی'] = get_update_date()

    # preprocess and create final df
    if mashaghel_type == 'heiat':

        agg_heiat = df_all.groupby(
            ['کد اداره', 'شهرستان', 'تاریخ بروزرسانی']).size()
        agg_heiat = agg_heiat.reset_index()
        agg_heiat['تاریخ بروزرسانی'] = get_update_date()

        agg_heiat.rename(
            columns={0: 'تعداد آماده ارسال به هیات مشاغل سنتی'}, inplace=True)
        # if save_on_folder:
        #     file_name = 'amade_ersal_beheiat_details.xlsx'
        #     output_dir = os.path.join(saved_folder, file_name)
        #     df_all.to_excel(output_dir)
        #     file_name = 'amade_ersal_beheiat_agg.xlsx'
        #     output_dir = os.path.join(saved_folder, file_name)
        #     agg_heiat.to_excel(output_dir)
        if save_how == 'db':
            drop_into_db(table_name='tblAmadeErsalBeHeiatMashSonati',
                         columns=df_all.columns.tolist(),
                         values=df_all.values.tolist(),
                         append_to_prev=False)
        agg_heiat = agg_heiat.rename(columns={'کد اداره': 'نام اداره سنتی'})
        return df_all, agg_heiat

    if (check_if_col_exists(df_all, 'تاريخ ثبت برگ تشخيص')):
        df_all['ماه صدور تشخیص'] = df_all['تاريخ ثبت برگ تشخيص'].str.slice(
            0, 6).astype('int64')

        if eblagh:
            df_all['ماه ابلاغ تشخیص'] = df_all['تاريخ ابلاغ برگ تشخيص'].str.slice(
                0, 6)
            if date is not None:
                df_all = df_all.loc[df_all['ماه ابلاغ تشخیص'].astype(
                    'int64') < date]
            # df_all_sodor = df_all.loc[df_all['ماه صدور تشخیص'] == '%s%s' % (year, month) ]
            # df_all_eblagh = df_all.loc[df_all['ماه ابلاغ تشخیص'] == '%s%s' % (year, month) ]
            agg_tashkhis_sodor = df_all.groupby(
                ['کد اداره', 'شهرستان', 'ماه صدور تشخیص', 'تاریخ بروزرسانی']).size()
            agg_tashkhis_eblagh = df_all.groupby(
                ['کد اداره', 'شهرستان', 'تاریخ بروزرسانی']).size()
            agg_tashkhis_sodor = agg_tashkhis_sodor.reset_index(level=0)
            agg_tashkhis_eblagh = agg_tashkhis_eblagh.reset_index()
            agg_tashkhis_sodor['تاریخ بروزرسانی'] = get_update_date()
            agg_tashkhis_eblagh['تاریخ بروزرسانی'] = get_update_date()
            agg_tashkhis_sodor = agg_tashkhis_sodor.reset_index(level=0)
            agg_tashkhis_sodor = agg_tashkhis_sodor.reset_index(level=0)
            agg_tashkhis_eblagh.rename(
                columns={0: 'تعداد تشخیص ابلاغی مشاغل سنتی'}, inplace=True)
            agg_tashkhis_sodor.rename(
                columns={0: 'تعداد تشخیص صادره مشاغل سنتی'}, inplace=True)

            # if save_on_folder:

            #     file_name_details_t_sadere = 'tashkhis_saderShode_details.xlsx'
            #     file_name_details = 'tashkhis_sadervaeblaghi_details.xlsx'
            #     file_name_agg_t_sadere = 'tashkhis_saderShode_agg.xlsx'
            #     file_name_details_t_eblaghi = 'tashkhis_eblaghshode_details.xlsx'
            #     file_name_agg_t_eblaghi = 'tashkhis_eblaghshode_agg.xlsx'
            #     output_dir = os.path.join(saved_folder, file_name_details)
            #     df_all.to_excel(output_dir)
            #     output_dir = os.path.join(saved_folder, file_name_agg_t_sadere)
            #     agg_tashkhis_sodor.to_excel(output_dir)
            #     output_dir = os.path.join(
            #         saved_folder, file_name_agg_t_eblaghi)
            #     agg_tashkhis_eblagh.to_excel(output_dir)

            if save_how == 'db':
                drop_into_db(table_name='tblTashkhisEblaghNoGhatee',
                             columns=df_all.columns.tolist(),
                             values=df_all.values.tolist(),
                             append_to_prev=False)
            # return df_all, agg_tashkhis_sodor, agg_tashkhis_eblagh
            agg_tashkhis_eblagh = agg_tashkhis_eblagh.rename(
                columns={'کد اداره': 'نام اداره سنتی'})
            return df_all, agg_tashkhis_eblagh

        else:
            if date is not None:
                df_all = df_all.loc[df_all['ماه صدور تشخیص'] < date]

            agg_tashkhis_sodor = df_all.groupby(
                ['کد اداره', 'شهرستان', 'تاریخ بروزرسانی']).size()
            agg_tashkhis_sodor = agg_tashkhis_sodor.reset_index()
            agg_tashkhis_sodor['تاریخ بروزرسانی'] = get_update_date()
            agg_tashkhis_sodor.rename(
                columns={0: 'تعداد تشخیص ابلاغ نشده مشاغل سنتی'}, inplace=True)
            if save_how == 'db':
                drop_into_db(table_name='tblTashkhisSodorNoElagh',
                             columns=df_all.columns.tolist(),
                             values=df_all.values.tolist(),
                             append_to_prev=False)

            agg_tashkhis_sodor = agg_tashkhis_sodor.rename(
                columns={'کد اداره': 'نام اداره سنتی'})

            return df_all, agg_tashkhis_sodor

    if (check_if_col_exists(df_all, 'تاريخ ثبت برگ قطعي')):
        df_all['ماه صدور قطعی'] = df_all['تاريخ ثبت برگ قطعي'].str.slice(
            0, 6).astype('int64')
        if eblagh:
            df_all['ماه ابلاغ قطعی'] = df_all['تاریخ ابلاغ برگ قطعی'].str.slice(
                0, 6)
            # df_all_sodor = df_all.loc[df_all['ماه صدور قطعی'] == '%s%s' % (year, month) ]
            # df_all_eblagh = df_all.loc[df_all['ماه ابلاغ قطعی'] == '%s%s' % (year, month) ]
            agg_ghatee_sodor = df_all.groupby(
                ['کد اداره', 'شهرستان', 'ماه صدور قطعی', 'تاریخ بروزرسانی']).size()
            agg_ghatee_eblagh = df_all.groupby(
                ['کد اداره', 'شهرستان', 'ماه ابلاغ قطعی', 'تاریخ بروزرسانی']).size()
            agg_ghatee_sodor = agg_ghatee_sodor.reset_index(level=0)
            agg_ghatee_eblagh = agg_ghatee_eblagh.reset_index(level=0)
            agg_ghatee_sodor['تاریخ بروزرسانی'] = get_update_date()
            agg_ghatee_eblagh['تاریخ بروزرسانی'] = get_update_date()
            agg_ghatee_sodor = agg_ghatee_sodor.reset_index(level=0)
            agg_ghatee_eblagh = agg_ghatee_eblagh.reset_index(level=0)
            agg_ghatee_sodor = agg_ghatee_sodor.reset_index(level=0)
            agg_ghatee_eblagh = agg_ghatee_eblagh.reset_index(level=0)
            agg_ghatee_eblagh.rename(
                columns={0: 'تعداد قطعی ابلاغی مشاغل سنتی'}, inplace=True)
            agg_ghatee_sodor.rename(
                columns={0: 'تعداد قطعی مشاغل سنتی'}, inplace=True)

            # if save_on_folder:

            #     file_name_details_g_sadere = 'ghatee_saderShode_details.xlsx'
            #     file_name_details = 'ghatee_sadervaeblaghi_details.xlsx'
            #     file_name_agg_g_sadere = 'ghatee_saderShode_agg.xlsx'
            #     file_name_details_g_eblaghi = 'ghatee_eblaghshode_details.xlsx'
            #     file_name_agg_g_eblaghi = 'ghatee_eblaghshode_agg.xlsx'
            #     output_dir = os.path.join(saved_folder, file_name_details)
            #     df_all.to_excel(output_dir)
            #     output_dir = os.path.join(saved_folder, file_name_agg_g_sadere)
            #     agg_ghatee_sodor.to_excel(output_dir)
            #     output_dir = os.path.join(
            #         saved_folder, file_name_agg_g_eblaghi)
            #     agg_ghatee_eblagh.to_excel(output_dir)

            if save_how == 'db':
                drop_into_db(table_name='tblGhateeSodorAndEblagh',
                             columns=df_all.columns.tolist(),
                             values=df_all.values.tolist(),
                             append_to_prev=False)

            agg_ghatee_sodor = agg_ghatee_sodor.rename(
                columns={'کد اداره': 'نام اداره سنتی'})

            agg_ghatee_eblagh = agg_ghatee_eblagh.rename(
                columns={'کد اداره': 'نام اداره سنتی'})

            return df_all, agg_ghatee_sodor, agg_ghatee_eblagh
        else:
            if date is not None:
                df_all = df_all.loc[df_all['ماه صدور قطعی'] < date]

            agg_ghatee_sodor = df_all.groupby(
                ['کد اداره', 'شهرستان', 'تاریخ بروزرسانی']).size()
            agg_ghatee_sodor = agg_ghatee_sodor.reset_index()
            agg_ghatee_sodor['تاریخ بروزرسانی'] = get_update_date()
            agg_ghatee_sodor.rename(
                columns={0: 'تعداد قطعی ابلاغ نشده مشاغل سنتی'}, inplace=True)

            if save_how == 'db':
                drop_into_db(table_name='tblGhateeSodorNoEblagh',
                             columns=df_all.columns.tolist(),
                             values=df_all.values.tolist(),
                             append_to_prev=False)

            agg_ghatee_sodor = agg_ghatee_sodor.rename(
                columns={'کد اداره': 'نام اداره سنتی'})

            return df_all, agg_ghatee_sodor


def drop_into_db(table_name, columns, values, append_to_prev=False, sql_con=get_sql_con()):
    if append_to_prev == False:
        # Deleting previous table
        delete_table = sql_delete(table_name)
        connect_to_sql(sql_query=delete_table, sql_con=sql_con,
                       connect_type='dropping sql table')
        # Creating new table
        sql_create_table = create_sql_table(
            table_name, columns)
        connect_to_sql(sql_create_table, sql_con=sql_con, connect_type='creating sql table')
    # Inserting data into table
    sql_query = insert_into(table_name, columns)
    connect_to_sql(sql_query, sql_con=sql_con, df_values=values,
                   connect_type='inserting into sql table')
# df1 = pd.read_excel(
#     r'C:\Users\alkav\Desktop\گزارش کارکرد\گزارش کارکرد جدید\ایریس\رسیدگی نشده ارزش افزوده سنیم New.xlsx')
# df2 = pd.read_excel(
#     r'C:\Users\alkav\Desktop\گزارش کارکرد\گزارش کارکرد جدید\ایریس\رسیدگی نشده ارزش افزوده سنیم.xlsx')

# df3 = df2.merge(df1, how='left', left_on=['شناسه اظهارنامه', 'سال عملکرد', 'دوره'], right_on=[
#                 'شماره اظهارنامه', 'سال عملکرد', 'دوره عملکرد'], indicator=True)

# df3.to_excel(
#     r'C:\Users\alkav\Desktop\گزارش کارکرد\گزارش کارکرد جدید\ایریس\رزوده سنیم.xlsx')


def process_mostaghelat(date=140106, report_type='Tashkhis', persian_name='تشخیص', sodor='صدور', msg='تشخیص ابلاغ نشده'):

    sql_query_edare_shahr = "SELECT [city],[edare] FROM [tax].[dbo].[tblEdareShahr]"
    sql_query_most = "SELECT * FROM tblMostaghelat%s" % report_type

    df_edare_shahr = connect_to_sql(sql_query_edare_shahr, sql_con=get_sql_con(
        database='tax'), read_from_sql=True, connect_type='read from tblEdateShahr', return_df=True)

    df_most_tashkhis = connect_to_sql(
        sql_query_most, read_from_sql=True, connect_type='read from tblMost', return_df=True)

    df_merged_1 = df_most_tashkhis.merge(df_edare_shahr, how='inner',
                                         left_on=df_most_tashkhis['واحد مالیاتی'].str.slice(
                                             0, 4),
                                         right_on='edare')

    df_merged_2 = df_most_tashkhis.merge(df_edare_shahr, how='inner',
                                         left_on=df_most_tashkhis['واحد مالیاتی'].str.slice(
                                             0, 5),
                                         right_on=df_edare_shahr['edare'].str.slice(0, 5)).drop(['key_0'], axis=1)

    df_f = pd.concat([df_merged_1, df_merged_2])
    df_f.drop_duplicates(subset=['شماره برگ %s' %
                         persian_name], keep=False, inplace=True)

    dff_final = df_f = pd.concat([df_f, df_merged_2])
    dff_final['ماه %s' % sodor] = dff_final['تاریخ %s' % sodor].str.replace(
        '/', '').str.slice(0, 6).astype('int64')
    dff_final = dff_final.loc[dff_final['ماه %s' % sodor] < 140106]
    dff_final.rename(columns={'edare': 'کد اداره',
                              'city': 'شهرستان'}, inplace=True)
    dff_final_agg = dff_final.groupby(
        ['کد اداره', 'شهرستان', 'تاریخ بروزرسانی']).size().reset_index()
    dff_final_agg.rename(
        columns={0: 'تعداد %s مستغلات' % msg}, inplace=True)
    return dff_final, dff_final_agg


def final_most(date=140106):
    tashkhis, tashkhis_agg = process_mostaghelat(date=date)
    ghatee, ghatee_agg = process_mostaghelat(date=date,
                                             report_type='Ghatee', persian_name='قطعی', msg='قطعی ابلاغ نشده')
    amade_ghatee, amade_ghatee_agg = process_mostaghelat(date=date,
                                                         report_type='AmadeGhatee', persian_name='تشخیص', sodor='ابلاغ', msg='آماده قطعی')

    lst_agg = [tashkhis_agg, ghatee_agg, amade_ghatee_agg]

    merged_agg = ft.reduce(lambda left, right: pd.merge(
        left, right, how='outer', on='کد اداره'), lst_agg)

    merged_agg['شهرستان'].fillna(merged_agg['شهرستان_y'], inplace=True)
    merged_agg['شهرستان'].fillna(merged_agg['شهرستان_x'], inplace=True)
    merged_agg['تاریخ بروزرسانی'].fillna(
        merged_agg['تاریخ بروزرسانی_x'], inplace=True)
    merged_agg['تاریخ بروزرسانی'].fillna(
        merged_agg['تاریخ بروزرسانی_y'], inplace=True)
    merged_agg['شهرستان'].fillna(merged_agg['شهرستان_x'], inplace=True)
    merged_agg.fillna(0, inplace=True)

    selected_columns = ['کد اداره',
                        'تعداد تشخیص ابلاغ نشده مستغلات',
                        'تعداد قطعی ابلاغ نشده مستغلات',
                        'شهرستان',
                        'تاریخ بروزرسانی',
                        'تعداد آماده قطعی مستغلات']

    merged_agg = merged_agg[selected_columns]
    merged_agg = merged_agg.rename(columns={'کد اداره': 'نام اداره سنتی'})
    merged_agg['نام اداره سنتی'] = merged_agg['نام اداره سنتی'].str.slice(0, 5)
    merged_agg = merged_agg.iloc[:, [0, 3, 1, 2, 5, 4]]

    return tashkhis, ghatee, amade_ghatee, merged_agg


def rename_duplicate_columns(df):

    cols = pd.Series(merged_agg.columns)
    for dup in merged_agg.columns[merged_agg.columns.duplicated(keep=False)]:
        cols[merged_agg.columns.get_loc(dup)] = (
            [dup + '.' + str(d_idx) if d_idx != 0 else dup for d_idx in range(merged_agg.columns.get_loc(dup).sum())])
    merged_agg.columns = cols

    return merged_agg
