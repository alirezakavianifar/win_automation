import os
from sanim import get_tashkhis_ghatee_sanim, get_badvi_sanim
from mashaghel_sonati import get_tashkhis_ghatee_sonati
from helpers import maybe_make_dir
from scrape import Scrape

path_arzeshafzoodeh = r'E:\automating_reports_V2\saved_dir\arzeshafzoodeh_sonati'
path_mostaghelat = r'E:\automating_reports_V2\saved_dir\mostaghelat'
path_codeghtesadi = r'E:\automating_reports_V2\saved_dir\codeghtesadi'

maybe_make_dir([path_arzeshafzoodeh])
maybe_make_dir([path_mostaghelat])
maybe_make_dir([path_codeghtesadi])


tashkhis_sonati, ghatee_sonati, amade_ersal_beheiat = get_tashkhis_ghatee_sonati(
    eblagh=False)
tashkhis_sonati, ghatee_sonati, amade_ersal_beheiat = get_tashkhis_ghatee_sonati(
    eblagh=True)
tashkhis_ghatee_sanim = get_tashkhis_ghatee_sanim()
badvi_sanim = get_badvi_sanim()

x = Scrape()
x.scrape_arzeshafzoodeh(path=path_arzeshafzoodeh)
x.scrape_codeghtesadi(path=path_codeghtesadi)
# x.scrape_mostaghelat(path=path_mostaghelat)

print('h')
