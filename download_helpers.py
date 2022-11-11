from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import glob
import sys
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import Login, login_sanim, maybe_make_dir, input_info, check_if_up_to_date, remove_excel_files, init_driver, log_it
from dump_to_sql import DumpToSQL
from sql_queries import create_sql_table, insert_into, create_sql_table, table_name


sources = ['مالیات بر درآمد شرکت ها','مالیات بر درآمد مشاغل','مالیات بر درآمد ارزش افزوده']

menu_nav_1000_p_1 = '/html/body/form/header/div[2]/div/ul/li[2]/div/div/div[2]/ul/li[3]/div[1]/span[1]/button'
menu_nav_1000_p_2 = '/html/body/form/header/div[2]/div/ul/li[2]/div/div/div[2]/ul/li[3]/div[2]/div/ul/li[2]/div/span[1]/span'
menu_nav_1000_year_input_1 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div/div[2]/div/span/span[1]/span/span[1]'
menu_nav_1000_year_input_2 = '/html/body/span/span/span[1]/input'
menu_nav_1000_year_input_3 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div[1]/div[2]/div[2]/button'
menu_nav_1000_source_input_1 = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div[1]/div[1]/div[3]/div/div[2]/div/span/span[1]/span'
menu_nav_1000_source_input_2 = '/html/body/span/span/span[1]/input'
menu_nav_1000_p_download_button = '/html/body/form/div[2]/div/div[2]/main/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div[2]/button[3]'





@log_it    
def download_excel(path=None, report_type=None, type_of_excel=None, no_files_in_path=None, excel_file=None):
    i = 0

    while len(glob.glob1(path, '%s' % excel_file)) == no_files_in_path:
       if i%60 == 0:
           print('waiting %s seconds for the file to be downloaded' % i)
       i+=1
       time.sleep(1)
    time.sleep(10)
   
    print('****************%s done*******************************' %type_of_excel)
    
    # excel_files = glob.glob1(path, '*.xlsx')
                 
            
    return path +'\\' + excel_file

# def download_excel():
#     try:
#         while(driver.find_element(By.CLASS_NAME, 'u-Processing-spinner')):
#             if i%60 == 0:
#                 print('waiting %s seconds for the file to be downloaded' % i)
#             i += 1
#             time.sleep(1)
            
#     except:
#             time.sleep(5)
#             j = j + 1
                
            
def download_1000_parvandeh(driver, report_type, year, path):

    WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_p_1)))
    driver.find_element(By.XPATH, menu_nav_1000_p_1).click() 
    time.sleep(1)
    WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_p_2)))
    driver.find_element(By.XPATH, menu_nav_1000_p_2).click()
    
    WebDriverWait(driver, 540).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_year_input_1)))
    driver.find_element(By.XPATH, menu_nav_1000_year_input_1).click()    
    
    WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_year_input_2)))
    driver.find_element(By.XPATH, menu_nav_1000_year_input_2).send_keys(year)
    driver.find_element(By.XPATH, menu_nav_1000_year_input_2).send_keys(Keys.RETURN)
    
    j = 0
    while j<len(sources):
        time.sleep(10)
        print('11')   
        WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_source_input_1)))
        driver.find_element(By.XPATH, menu_nav_1000_source_input_1).click()   
        print('22')
        WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_source_input_2)))
        driver.find_element(By.XPATH, menu_nav_1000_source_input_2).send_keys(sources[j])
        driver.find_element(By.XPATH, menu_nav_1000_source_input_2).send_keys(Keys.RETURN)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_year_input_3)))
        driver.find_element(By.XPATH, menu_nav_1000_year_input_3).click()
        time.sleep(2)
        
        try:
            
            while (driver.find_element(By.CLASS_NAME, 'u-Processing-spinner')):
                
                time.sleep(1)
                
            
        except Exception as e :
            time.sleep(3)
            
            # try:
                
                # if (driver.find_element(By.XPATH, '//*[@id="ANNUAL_TAXTYPE_data_panel"]/div/div/span')):
                #     print('list empty')
                #     j = j + 1
                #     continue
            # except:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, menu_nav_1000_p_download_button)))
            driver.find_element(By.XPATH, menu_nav_1000_p_download_button).click()
            
            download_excel(path=path, report_type=report_type, type_of_excel='', no_files_in_path=j)
            
            j += 1
            print('j = %s' % j)
            
                    
                    
                    
def download_tabsare_100():
    
    pass
    #     self.driver.find_element(By.XPATH, menu_nav_1).click()
    #     time.sleep(2)
    #     self.driver.find_element(By.XPATH, '//*[@id="t_MenuNav_1_1_0i"]').click()
        
    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, td_5)))
    #     self.driver.find_element(By.XPATH, td_5).click()

    #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, input_1)))
    #     self.driver.find_element(By.XPATH, input_1).send_keys(self.year)
        
    #     time.sleep(2)
        
        
    #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, input_1)))
    #     self.driver.find_element(By.XPATH, input_1).send_keys(Keys.ENTER)
        
    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, '%s/td[4]/a' % td_3)))
    #     self.driver.find_element(By.XPATH, '%s/td[4]/a' % td_3).click()
    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, td_4)))

    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, year_button_6)))
    #     self.driver.find_element(By.XPATH, year_button_6).click()

    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH,year_button_4)))
    #     self.driver.find_element(By.XPATH,year_button_4).click()

    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, year_button_5)))
    #     self.driver.find_element(By.XPATH, year_button_5).click()

    #     self.download_excel('Tabsare 100', 0)
        
    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, '%s/td[5]/a' % td_3)))
    #     self.driver.find_element(By.XPATH, '%s/td[5]/a' % td_3).click()
    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, td_4)))

    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, year_button_6)))
    #     self.driver.find_element(By.XPATH, year_button_6).click()

    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH,year_button_4)))
    #     self.driver.find_element(By.XPATH,year_button_4).click()

    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, year_button_5)))
    #     self.driver.find_element(By.XPATH, year_button_5).click()
        
        
    #     self.download_excel('Tabsare 100', 1)
        
    #     time.sleep(5)
        
    #     self.driver.back()
        
    #     time.sleep(5)
                    
    #     self.driver.back()
        
    #     time.sleep(10)

    #     self.driver.back()

    #     self.driver.find_element(By.XPATH, menu_nav_1).click()
    #     time.sleep(2)
    #     self.driver.find_element(By.XPATH, '//*[@id="t_MenuNav_1_1_1i"]').click()
        
    #     time.sleep(40)
            
    #     WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, td_6)))
    #     self.driver.find_element(By.XPATH, td_6).click()
        
    #     WebDriverWait(self.driver, 45).until(EC.presence_of_element_located((By.XPATH, input_1)))
    #     self.driver.find_element(By.XPATH, input_1).send_keys(self.year)
        
    #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, input_1)))
    #     self.driver.find_element(By.XPATH, input_1).send_keys(Keys.ENTER)
        
    #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '%s/td[3]/a' % td_2)))
    #     self.driver.find_element(By.XPATH, '%s/td[3]/a' % td_2).click()
        
    #     WebDriverWait(self.driver, time_out_2).until(EC.presence_of_element_located((By.XPATH, download_button)))
    #     self.driver.find_element(By.XPATH, download_button).click()

    #     self.download_excel('final file', 2)               
    #     return