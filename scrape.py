from selenium.webdriver.common.by import By
import time
import glob
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from helpers import login_sanim, login_arzeshafzoodeh, login_tgju,\
    login_mostaghelat, login_codeghtesadi, login_scholar, login_scihub,\
    maybe_make_dir, input_info, merge_multiple_excel_sheets, \
    remove_excel_files, init_driver, \
    log_it, is_updated_to_download, \
    is_updated_to_save, rename_files, merge_multiple_html_files, merge_multiple_excel_files
from download_helpers import download_1000_parvandeh, download_excel
from constants import get_dict_years
import threading
from watchdog_186 import watch_over, is_downloaded

start_index = 1
n_retries = 0
first_list = [4, 5, 6, 7, 8, 9, 10, 21, 22, 23, 24]
second_list = [14, 15, 16, 17]
time_out_1 = 2080
time_out_2 = 2080
timeout_fifteen = 15
excel_file_names = ['Excel.xlsx', 'Excel(1).xlsx', 'Excel(2).xlsx']
badvi_file_names = ['جزئیات اعتراضات و شکایات.html']


download_button_ezhar = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div/div/div[2]/div[1]/div[2]/button[3]'
download_button_rest = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/font/div/div/div[2]/div[1]/div[2]/button[2]'
menu_nav_1 = '//*[@id="t_MenuNav_1_1i"]'
menu_nav_2 = '/html/body/form/header/div[2]/div/ul/li[2]/div/div/div[2]/ul/li[1]/div/span[1]/a'
# menu_nav_2 = '/html/body/form/header/div[2]/div/ul/li[2]/div/div/ul/li[1]/div/span[1]/a'
year_button_1 = '//*[@id="P1100_TAX_YEAR_CONTAINER"]/div[2]/div/div'
year_button_2 = '/html/body/div[7]/div[2]/div[1]/button'
year_button_3 = '/html/body/div[7]/div[2]/div[2]/div/div[3]/ul/li'
year_button_4 = '/html/body/div[3]/div/ul/li[8]/div/span[1]/button'
switch_to_data = '/html/body/div[6]/div[2]/div[2]/div/div/div/div[2]/label/span'
download_excel_btn_1 = '/html/body/div[6]/div[2]/ul/li[1]/span[1]'
download_excel_btn_2 = '/html/body/div[6]/div[3]/div/button[2]'
input_1 = '/html/body/span/span/span[1]/input'
td_1 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/font/div/div/div[2]/div[2]/div[5]/div[1]/div/div[3]/table/tbody/tr[2]'
td_2 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/font/div[2]/div/div[2]/div[2]/div[5]/div[1]/div/div[2]/table/tbody/tr[2]'
td_3 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div[5]/div[1]/div/div[2]/table/tbody/tr[2]'
year_button_5 = '/html/body/div[6]/div[3]/div/button[2]'
year_button_6 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div/div/div[2]/div[1]/div[1]/div[3]/div/button'
td_4 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[5]/div[1]/div/div[1]/table/tr/th[8]/a'
td_5 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/span/span[1]/span/span[2]'
td_6 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/font/div[1]/div/div/div/div[2]/div/span/span[1]/span/span[1]'
td_ezhar = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[5]/div[1]/div/div[2]/table/tbody/tr[2]/td[%s]/a'


def retry(func):
    def try_it(Cls):
        global n_retries
        try:
            result = func(Cls)
            return result

        except Exception as e:
            n_retries += 1
            print(e)
            if n_retries < 50:
                print('trying again')
                Cls.driver.close()
                path = Cls.path
                report_type = Cls.report_type
                year = Cls.year
                time.sleep(3)
                x = Scrape(path, report_type, year)
                x.scrape_sanim()

    return try_it


class Scrape:

    def __init__(self, path=None, report_type=None, year=None, driver_type='firefox'):
        self.path = path
        self.report_type = report_type
        self.year = year
        self.driver_type = driver_type

    def scrape_scihub(self, path=None, return_df=True, headless=False, search_term='all'):

        try:
            self.driver = init_driver(
                pathsave=path, driver_type=self.driver_type, headless=headless)
            self.path = path
            self.driver = login_scihub(self.driver)
            # Enter the search term
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.NAME, 'request')))
            self.driver.find_element(
                By.NAME, 'request').send_keys(search_term)
            # Enter the search button
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.TAG_NAME, 'button')))
            self.driver.find_element(
                By.TAG_NAME, 'button').click()
            time.sleep(3)
            # Close ads
            # if (self.driver.find_element(
            #         By.ID, 'close').is_displayed()):
            #     self.driver.find_element(
            #         By.ID, 'close').click()
            # time.sleep(0.5)

            # Click the download button
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[1]/button')))
            self.driver.find_element(
                By.XPATH, '/html/body/div[3]/div[1]/button').click()
            time.sleep(5)
            self.driver.quit()
            # WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
            #     (By.ID, 'download')))
            # self.driver.find_element(
            #     By.ID, 'download').click()
            # time.sleep(5)

            # self.driver.back()
            # Go back to the start page
            # WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
            #     (By.ID, 'sci')))
            # self.driver.find_element(
            #     By.ID, 'sci').click()

        except Exception as e:
            print(e)

    def scrape_scholar(self, path=None, return_df=True, headless=False, search_term='all'):
        lst_cites = []
        lst_links = []
        try:

            self.driver = init_driver(
                pathsave=path, driver_type=self.driver_type, headless=headless)
            self.path = path
            self.driver = login_scholar(self.driver)

            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.ID, 'gs_hdr_tsi')))
            self.driver.find_element(
                By.ID, 'gs_hdr_tsi').send_keys(search_term)

            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div/div[7]/div[1]/div[2]/form/button/span/span[1]')))
            self.driver.find_element(
                By.XPATH, '/html/body/div/div[7]/div[1]/div[2]/form/button/span/span[1]').click()

            # Wait for captcha
            try:
                if (self.driver.find_element(
                        By.ID, 'gs_captcha_f')):
                    while (self.driver.find_element(
                            By.ID, 'gs_captcha_f')):
                        print('waiting for captcha')
                time.sleep(2)
            # continue after completing captcha
            except:

                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[2]/div[1]/div[2]/div[3]/a[3]')))
                self.driver.find_element(
                    By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[2]/div[1]/div[2]/div[3]/a[3]').click()

                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, 'gs_or_cit')))
                cites = self.driver.find_elements(
                    By.CLASS_NAME, 'gs_or_cit')

                # Get links of citations
                links = self.driver.find_elements(
                    By.CLASS_NAME, 'gs_ri')

                def get_links(links):
                    links = [link.find_element(By.TAG_NAME, 'a')
                             for link in links]
                    links = [elem.get_attribute('href') for elem in links]
                    return links

                lst_links.extend(get_links(links))

                def scrape_cites(cites):
                    for index, cite in enumerate(cites):

                        WebDriverWait(cite, 8).until(EC.presence_of_element_located(
                            (By.TAG_NAME, 'span')))
                        element = cite.find_element(
                            By.TAG_NAME, 'span')
                        self.driver.execute_script(
                            "arguments[0].click();", element)

                        # Get the text of the citation
                        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                            (By.XPATH, '/html/body/div/div[4]/div/div[2]/div/div[1]/table/tbody/tr[4]/td/div')))
                        time.sleep(1)
                        lst_cites.append(self.driver.find_element(
                            By.XPATH, '/html/body/div/div[4]/div/div[2]/div/div[1]/table/tbody/tr[4]/td/div').text)

                        # Close openend window
                        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                            (By.ID, 'gs_cit-x')))

                        element = self.driver.find_element(
                            By.ID, 'gs_cit-x')
                        time.sleep(1)
                        self.driver.execute_script(
                            "arguments[0].click();", element)

                        time.sleep(1)

                scrape_cites(cites)

                try:
                    # Go to the next page
                    time.sleep(1)
                    WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[3]/div[2]/center/table/tbody/tr/td[11]/a/b')))
                    while (self.driver.find_element(
                            By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[3]/div[2]/center/table/tbody/tr/td[11]/a/b')):
                        self.driver.find_element(
                            By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[3]/div[2]/center/table/tbody/tr/td[11]/a/b').click()

                        # Get links of citations
                        links = self.driver.find_elements(
                            By.CLASS_NAME, 'gs_ri')
                        lst_links.extend(get_links(links))
                        # Locate citations
                        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                            (By.CLASS_NAME, 'gs_or_cit')))
                        cites = self.driver.find_elements(
                            By.CLASS_NAME, 'gs_or_cit')
                        # Scrape cites
                        scrape_cites(cites)
                except Exception as e:
                    return lst_cites, lst_links

            return lst_cites, lst_links

        except Exception as e:
            print(e)

    def scrape_tgju(self, path=None, return_df=True, headless=False):
        try:
            self.driver = init_driver(
                pathsave=path, driver_type=self.driver_type, headless=headless)
            self.path = path
            self.driver = login_tgju(self.driver)
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[5]/span[1]/span')))
            price = self.driver.find_element(
                By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[5]/span[1]/span').text
            WebDriverWait(self.driver, 540).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/header/div[2]/div[6]/ul/li/a/img')))
            try:
                if (self.driver.find_element(
                        By.XPATH, '/html/body/div[2]/header/div[2]/div[6]/ul/li/a/img')):
                    time.sleep(5)
                    WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[5]/span[1]/span')))
                    coin = self.driver.find_element(
                        By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[5]/span[1]/span').text

                    WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[6]/span[1]/span')))
                    dollar = self.driver.find_element(
                        By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[6]/span[1]/span').text

                    WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[4]/span[1]/span')))
                    gold = self.driver.find_element(
                        By.XPATH, '/html/body/main/div[1]/div[2]/div/ul/li[4]/span[1]/span').text
            except Exception as e:
                print(e)

            self.driver.close()
        except Exception as e:
            self.driver.close()

        return coin, dollar, gold

    def scrape_codeghtesadi(self, path=None, return_df=True):
        self.driver = init_driver(
            pathsave=path, driver_type=self.driver_type)
        self.path = path
        self.driver = login_codeghtesadi(self.driver)
        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/form/table/tbody/tr[2]/td[1]/a[2]/div')))
        self.driver.find_element(
            By.XPATH, '/html/body/form/table/tbody/tr[2]/td[1]/a[2]/div').click()
        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/span[2]/div[2]/table/tbody/tr/td[2]/div/span')))
        self.driver.find_element(
            By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/span[2]/div[2]/table/tbody/tr/td[2]/div/span').click()

        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/span[2]/div[2]/table/tbody/tr/td[2]/div/div/a[1]')))
        self.driver.find_element(
            By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/span[2]/div[2]/table/tbody/tr/td[2]/div/div/a[1]').click()

        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/span[2]/div/a')))
        self.driver.find_element(
            By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/span[2]/div/a').click()

        time.sleep(10)

        file_list = glob.glob(self.path + "/*" + '.xls.part')

        while len(file_list) != 0:

            time.sleep(1)
            file_list = glob.glob(self.path + "/*" + '.xls.part')

        merge_multiple_excel_sheets(self.path, dest=self.path)

    def scrape_mostaghelat(self, path=None, report_type='tashkhis', return_df=False, table_name=None, drop_to_sql=True, append_to_prev=False):
        def scrape_it():
            self.driver = init_driver(
                pathsave=path, driver_type=self.driver_type)
            self.path = path
            self.driver = login_mostaghelat(self.driver)
            WebDriverWait(self.driver, 66).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/form/div[4]/div[1]/ul[1]/li[10]/a/span')))
            time.sleep(5)
            self.driver.find_element(
                By.XPATH, '/html/body/form/div[4]/div[1]/ul[1]/li[10]/a/span').click()
            if report_type == 'amade_ghatee':
                index = '15'
                select_type = 'Dro_S_TaxOffice'
            elif report_type == 'tashkhis':
                index = '8'
                select_type = 'Drop_S_TaxUnitCode'
            elif report_type == 'ghatee':
                path_second_date = '/html/body/form/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div/div/div[2]/table[1]/tbody/tr[3]/td[4]/button'
                index = '9'
                select_type = 'Drop_S_TaxUnitCode'

            WebDriverWait(self.driver, 24).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/form/div[4]/div[1]/ul[1]/li[10]/ul/li[%s]/a/i[2]' % index)))
            self.driver.find_element(
                By.XPATH, '/html/body/form/div[4]/div[1]/ul[1]/li[10]/ul/li[%s]/a/i[2]' % index).click()
            if select_type == 'Drop_S_TaxUnitCode':
                time.sleep(3)
                WebDriverWait(self.driver, 48).until(EC.presence_of_element_located(
                    (By.ID, 'Txt_RegisterDateAz')))
                # time.sleep(5)
                self.driver.find_element(
                    By.ID, 'Txt_RegisterDateAz').click()
                time.sleep(1)
                sel = Select(self.driver.find_element(
                    By.ID, 'bd-year-Txt_RegisterDateAz'))
                sel.select_by_index(0)
                WebDriverWait(self.driver, 24).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, 'day-1')))
                self.driver.find_element(
                    By.CLASS_NAME, 'day-1').click()

                WebDriverWait(self.driver, 24).until(EC.presence_of_element_located(
                    (By.ID, 'Txt_RegisterDateTa')))
                self.driver.find_element(
                    By.ID, 'Txt_RegisterDateTa').click()
                sel = Select(self.driver.find_element(
                    By.ID, 'bd-year-Txt_RegisterDateTa'))
                sel.select_by_index(99)
                if report_type == 'tashkhis':
                    WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[3]/div/div/div[2]/table[1]/tbody/tr[1]/td[7]/button')))
                    self.driver.find_element(
                        By.XPATH, '/html/body/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[3]/div/div/div[2]/table[1]/tbody/tr[1]/td[7]/button').click()

                else:
                    WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                        (By.XPATH, path_second_date)))
                    self.driver.find_element(
                        By.XPATH, path_second_date).click()

            if report_type == 'amade_ghatee':

                sel = Select(self.driver.find_element(By.ID, select_type))
                count = len(sel.options) - 1
            else:
                count = 1

            def mostagh(i, select_type=select_type):

                if report_type == 'amade_ghatee':
                    sel = Select(self.driver.find_element(By.ID, select_type))
                    sel.select_by_index(i)

                WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(
                    (By.ID, 'Btn_Search')))
                self.driver.find_element(
                    By.ID, 'Btn_Search').click()
                if report_type == 'amade_ghatee':
                    try:
                        if (self.driver.find_element(By.ID, 'ContentPlaceHolder1_Btn_Export')):
                            time.sleep(4)
                            self.driver.find_element(
                                By.ID, 'ContentPlaceHolder1_Btn_Export').click()
                    except Exception as e:
                        global start_index
                        start_index += 1
                        mostagh(start_index, select_type=select_type)

                elif (self.driver.find_element(By.ID, 'ContentPlaceHolder1_Lbl_Count').text != 'تعداد : 0 مورد'):
                    try:
                        if (self.driver.find_element(By.ID, 'ContentPlaceHolder1_Btn_Export')):
                            time.sleep(4)
                            self.driver.find_element(
                                By.ID, 'ContentPlaceHolder1_Btn_Export').click()
                    except Exception as e:
                        print(e)

            global start_index
            while start_index <= count:
                try:
                    t1 = threading.Thread(target=mostagh, args=(start_index,))
                    t2 = threading.Thread(target=watch_over, args=(self.path,))
                    t1.start()
                    t2.start()
                    t1.join()
                    t2.join()
                    start_index += 1
                except Exception as e:
                    print(e)
                    continue

        scrape_it()

        df = merge_multiple_excel_files(
            self.path,
            self.path,
            table_name=table_name,
            delete_after_merge=True,
            postfix='xls',
            drop_to_sql=drop_to_sql,
            append_to_prev=append_to_prev)

        if return_df:
            return df

        self.driver.close()

    def scrape_arzeshafzoodeh(self, path=None, return_df=True, del_prev_files=True):
        def scrape_it():
            if del_prev_files:
                remove_excel_files(file_path=path, postfix='.xls')
            self.driver = init_driver(
                pathsave=path, driver_type=self.driver_type)
            self.path = path
            self.driver = login_arzeshafzoodeh(self.driver)
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/form/div[3]/table/tbody/tr[2]/td/div/table/tbody/tr[10]/td/div/ul/li[10]/a/span')))
            self.driver.find_element(
                By.XPATH, '/html/body/form/div[3]/table/tbody/tr[2]/td/div/table/tbody/tr[10]/td/div/ul/li[10]/a/span').click()
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/form/div[3]/table/tbody/tr[2]/td/div/table/tbody/tr[10]/td/div/ul/li[10]/div/ul/li[16]/a/span')))
            self.driver.find_element(
                By.XPATH, '/html/body/form/div[3]/table/tbody/tr[2]/td/div/table/tbody/tr[10]/td/div/ul/li[10]/div/ul/li[16]/a/span').click()

            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.ID, 'ctl00_ContentPlaceHolder1_chkAuditStatus_2')))
            self.driver.find_element(
                By.ID, 'ctl00_ContentPlaceHolder1_chkAuditStatus_2').click()
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.ID, 'ctl00_ContentPlaceHolder1_chkAuditStatus_3')))
            self.driver.find_element(
                By.ID, 'ctl00_ContentPlaceHolder1_chkAuditStatus_3').click()

            def arzesh(i):
                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.ID, 'ctl00_ContentPlaceHolder1_frm_year')))
                sel = Select(self.driver.find_element(
                    By.ID, 'ctl00_ContentPlaceHolder1_frm_year'))
                sel.select_by_index(i)

                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.ID, 'ctl00_ContentPlaceHolder1_frm_period')))
                sel = Select(self.driver.find_element(
                    By.ID, 'ctl00_ContentPlaceHolder1_frm_period'))
                sel.select_by_index(0)

                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.ID, 'ctl00_ContentPlaceHolder1_To_year')))
                sel = Select(self.driver.find_element(
                    By.ID, 'ctl00_ContentPlaceHolder1_To_year'))
                sel.select_by_index(i)

                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.ID, 'ctl00_ContentPlaceHolder1_To_period')))
                sel = Select(self.driver.find_element(
                    By.ID, 'ctl00_ContentPlaceHolder1_To_period'))
                sel.select_by_index(3)

                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.ID, 'ctl00_ContentPlaceHolder1_Button3')))
                time.sleep(10)
                self.driver.find_element(
                    By.ID, 'ctl00_ContentPlaceHolder1_Button3').click()

            for i in range(0, 15):

                t1 = threading.Thread(target=arzesh, args=(i,))
                t2 = threading.Thread(target=watch_over)
                t1.start()
                t2.start()
                t1.join()
                t2.join()

            file_list = glob.glob(self.path + "/*" + '.xls.part')

            while len(file_list) != 0:

                time.sleep(1)
                file_list = glob.glob(self.path + "/*" + '.xls.part')

        # scrape_it()

        time.sleep(1)
        dest = os.path.join(path, 'temp')
        dest = path
        rename_files(path, dest=dest)
        df_arzesh = merge_multiple_html_files(
            path=dest, drop_into_sql=True, drop_to_excel=True)

        if return_df:
            return df_arzesh

    @retry
    def scrape_sanim(self):
        self.driver = init_driver(
            pathsave=path, driver_type=self.drive_type)
        global excel_file_names

        self.driver = login_sanim(self.driver)

        if self.report_type == 'ezhar':
            download_button = download_button_ezhar
        else:
            download_button = download_button_rest

        # انتخاب منوی گزارشات اصلی

        self.driver.find_element(
            By.XPATH, '/html/body/form/header/div[2]/div/ul/li[2]/span/span').click()
        time.sleep(1)
        self.driver.find_element(
            By.XPATH, '/html/body/form/header/div[2]/div/ul/li[2]/button').click()
        if self.report_type != 'tabsare_100':

            if (self.report_type == 'ezhar'):
                td_number = 4
            elif (self.report_type == 'hesabrasi_darjarian_before5'):
                td_number = 5
            elif (self.report_type == 'hesabrasi_darjarian_after5'):
                td_number = 6
            elif (self.report_type == 'hesabrasi_takmil_shode'):
                td_number = 7
            elif (self.report_type == 'tashkhis_sader_shode'):
                td_number = 8
            elif (self.report_type == 'tashkhis_eblagh_shode'):
                td_number = 9
            elif (self.report_type == 'tashkhis_eblagh_nashode'):
                td_number = 10
            elif (self.report_type == 'ghatee_sader_shode'):
                td_number = 21
            elif (self.report_type == 'ghatee_eblagh_shode'):
                td_number = 22
            elif (self.report_type == 'ejraee_sader_shode'):
                td_number = 23
            elif (self.report_type == 'ejraee_eblagh_shode'):
                td_number = 24
            elif (self.report_type == 'badvi_darjarian_dadrasi'):
                td_number = 15
            elif (self.report_type == 'badvi_takmil_shode'):
                td_number = 16
            elif (self.report_type == 'tajdidnazer_darjarian_dadrasi'):
                td_number = 17
            elif (self.report_type == 'tajdidnazar_takmil_shode'):
                td_number = 18

            if (self.report_type == '1000_parvande'):

                download_1000_parvandeh(
                    self.driver, self.report_type, self.year, self.path)

            else:
                # انتخاب منوی اول از گزارشات اصلی
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, menu_nav_2)))
                self.driver.find_element(By.XPATH, menu_nav_2).click()

                # انتخاب سال عملکرد
                # WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.XPATH, year_button_1)))
                # self.driver.find_element(By.XPATH,year_button_1).click()
                time.sleep(4)
                WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.ID, 'P1100_TAX_YEAR')))
                self.driver.find_element(By.ID, 'P1100_TAX_YEAR').click()

                time.sleep(3)
                WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[7]/div[2]/div[1]/input')))
                self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div[2]/div[1]/input').send_keys(self.year)

                WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, year_button_2)))
                self.driver.find_element(By.XPATH, year_button_2).click()

                time.sleep(3)

                WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, year_button_3)))
                self.driver.find_element(By.XPATH, year_button_3).click()

                #################################################################################################################################

                time.sleep(3)

                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '%s/td[4]/a' % td_2)))
                self.driver.find_element(
                    By.XPATH, '%s/td[%s]/a' % (td_2, td_number)).click()

                time.sleep(4)

                # دریافت اظهارنامه ها و تشخیص های صادر شده
                exists_in_first_list = first_list.count(td_number)

                if (exists_in_first_list):

                    # print(check_if_up_to_date('%s\%s' % (self.path, excel_file_names[0])))

                    if not (is_updated_to_download('%s\%s' % (self.path, excel_file_names[0]))):
                        # if(uptodate.count(self.path + '\Excel.xlsx') == 0):
                        print('updating for report_type=%s and year=%s' %
                              (self.report_type, self.year))
                        # WebDriverWait(self.driver, time_out_1).until(EC.presence_of_element_located((By.XPATH, '%s/td[4]/a' % td_1)))
                        # self.driver.find_element(By.XPATH, '%s/td[5]/a' % td_1).click()
                        if (self.report_type != 'ezhar'):
                            WebDriverWait(self.driver, timeout_fifteen).until(
                                EC.presence_of_element_located((By.XPATH, '%s/td[4]/a' % td_1)))
                            self.driver.find_element(
                                By.XPATH, '%s/td[4]/a' % td_1).click()

                        else:
                            WebDriverWait(self.driver, timeout_fifteen).until(
                                EC.presence_of_element_located((By.XPATH, td_ezhar % 5)))
                            self.driver.find_element(
                                By.XPATH, td_ezhar % 5).click()

                        time.sleep(4)
                        WebDriverWait(self.driver, time_out_2).until(
                            EC.presence_of_element_located((By.XPATH, download_button)))
                        self.driver.find_element(
                            By.XPATH, download_button).click()

                        print(
                            '*******************************************************************************************')
                        download_excel(path=self.path, report_type=self.report_type,
                                       type_of_excel='Hoghoghi', no_files_in_path=0, excel_file=excel_file_names[0])
                        self.driver.back()

                    if not (is_updated_to_download('%s\%s' % (self.path, excel_file_names[1]))):
                        print('updating for report_type=%s and year=%s' %
                              (self.report_type, self.year))
                        if (self.report_type != 'ezhar'):
                            WebDriverWait(self.driver, timeout_fifteen).until(
                                EC.presence_of_element_located((By.XPATH, '%s/td[3]/a' % td_1)))
                            self.driver.find_element(
                                By.XPATH, '%s/td[3]/a' % td_1).click()

                        else:
                            WebDriverWait(self.driver, timeout_fifteen).until(
                                EC.presence_of_element_located((By.XPATH, td_ezhar % 4)))
                            self.driver.find_element(
                                By.XPATH, td_ezhar % 4).click()

                        time.sleep(4)
                        WebDriverWait(self.driver, time_out_1).until(
                            EC.presence_of_element_located((By.XPATH, download_button)))
                        self.driver.find_element(
                            By.XPATH, download_button).click()

                        print(
                            '*******************************************************************************************')

                        download_excel(path=self.path, report_type=self.report_type,
                                       type_of_excel='Haghighi', no_files_in_path=0, excel_file=excel_file_names[1])
                        self.driver.back()

                    if not (is_updated_to_download('%s\%s' % (self.path, excel_file_names[2]))):
                        print('updating for report_type=%s and year=%s' %
                              (self.report_type, self.year))
                        if (self.report_type != 'ezhar'):
                            WebDriverWait(self.driver, timeout_fifteen).until(
                                EC.presence_of_element_located((By.XPATH, '%s/td[7]/a' % td_1)))
                            self.driver.find_element(
                                By.XPATH, '%s/td[7]/a' % td_1).click()
                        else:
                            WebDriverWait(self.driver, timeout_fifteen).until(
                                EC.presence_of_element_located((By.XPATH, td_ezhar % 8)))
                            self.driver.find_element(
                                By.XPATH, td_ezhar % 8).click()

                        time.sleep(4)
                        WebDriverWait(self.driver, time_out_1).until(
                            EC.presence_of_element_located((By.XPATH, download_button)))
                        self.driver.find_element(
                            By.XPATH, download_button).click()

                        print(
                            '*******************************************************************************************')

                        download_excel(path=self.path, report_type=self.report_type,
                                       type_of_excel='Arzesh Afzoode', no_files_in_path=0, excel_file=excel_file_names[2])
                        self.driver.back()

                # if there is only one report and no distinction between haghighi, hoghoghi and arzesh afzoode
                else:

                    time.sleep(3)
                    WebDriverWait(self.driver, time_out_2).until(
                        EC.presence_of_element_located((By.XPATH, year_button_6)))
                    self.driver.find_element(By.XPATH, year_button_6).click()
                    time.sleep(1)
                    WebDriverWait(self.driver, time_out_2).until(
                        EC.presence_of_element_located((By.XPATH, year_button_4)))
                    self.driver.find_element(By.XPATH, year_button_4).click()
                    time.sleep(0.5)
                    WebDriverWait(self.driver, time_out_2).until(
                        EC.presence_of_element_located((By.XPATH, switch_to_data)))
                    self.driver.find_element(By.XPATH, switch_to_data).click()
                    time.sleep(0.5)
                    WebDriverWait(self.driver, time_out_2).until(
                        EC.presence_of_element_located((By.XPATH, download_excel_btn_1)))
                    self.driver.find_element(
                        By.XPATH, download_excel_btn_1).click()
                    time.sleep(0.5)
                    WebDriverWait(self.driver, time_out_2).until(
                        EC.presence_of_element_located((By.XPATH, download_excel_btn_2)))
                    self.driver.find_element(
                        By.XPATH, download_excel_btn_2).click()
                    download_excel(path=self.path, report_type=self.report_type,
                                   type_of_excel=self.report_type, no_files_in_path=0, excel_file=badvi_file_names[0])

        # else:

        time.sleep(180)
        self.driver.close()
