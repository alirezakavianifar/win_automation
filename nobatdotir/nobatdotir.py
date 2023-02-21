from import_nobatdotir import import_nobatdotir
sys, pd, Scrape, maybe_make_dir, get_update_date, drop_into_db, get_sql_con, time, datetime  = import_nobatdotir()


path = r'D:\projects\win_automation\saved_dir\nobatdotir'


def scrape_nobatdotir():
    nobat = Scrape()
    nobat.scrape_nobatdotir(path=path)
    print('done')
    
scrape_nobatdotir()