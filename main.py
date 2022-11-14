import functools as ft
import os
import pandas as pd
from sanim import get_tashkhis_ghatee_sanim, get_badvi_sanim
from mashaghel_sonati import get_tashkhis_ghatee_sonati
from helpers import maybe_make_dir, connect_to_sql, final_most
from scrape import Scrape
from constants import get_sql_con

path_arzeshafzoodeh = r'E:\automating_reports_V2\saved_dir\arzeshafzoodeh_sonati'
path_mostaghelat = r'E:\automating_reports_V2\saved_dir\mostaghelat'
path_mostaghelat_tashkhis = r'E:\automating_reports_V2\saved_dir\mostaghelat\mostaghelat_tashkhis'
path_mostaghelat_ghatee = r'E:\automating_reports_V2\saved_dir\mostaghelat\mostaghelat_ghatee'
path_mostaghelat_amade_ghatee = r'E:\automating_reports_V2\saved_dir\mostaghelat\mostaghelat_amade_ghatee'
path_codeghtesadi = r'E:\automating_reports_V2\saved_dir\codeghtesadi'

maybe_make_dir([path_arzeshafzoodeh])
maybe_make_dir([path_mostaghelat])
maybe_make_dir([path_mostaghelat_tashkhis])
maybe_make_dir([path_mostaghelat_ghatee])
maybe_make_dir([path_mostaghelat_amade_ghatee])
maybe_make_dir([path_codeghtesadi])


tashkhis_saderNashode, agg_tashkhis_saderNashode, ghatee_saderNashode, agg_ghatee_saderNashode, amade_ersal_beheiat, agg_amade_ersal_beheiat, tashkhis_eblagh_noGhatee, agg_tashkhis_eblagh_noGhatee = get_tashkhis_ghatee_sonati(
    eblagh=False)


# tashkhis_sadere, ghatee_sadere, tashkhis_eblaghi, ghatee_eblaghi = get_tashkhis_ghatee_sonati(
#     eblagh=True)

tashkhis_sanim, ghatee_sanim, agg_tashkhis_ghatee_sanim = get_tashkhis_ghatee_sanim()

badvi_sanim, agg_badvi_sanim = get_badvi_sanim()

# x = Scrape()
# x.scrape_arzeshafzoodeh(path=path_arzeshafzoodeh)
# x.scrape_codeghtesadi(path=path_codeghtesadi)
# x.scrape_mostaghelat(path=path_mostaghelat_tashkhis,
#                      report_type='tashkhis', table_name='tblMostaghelatTashkhis', append_to_prev=False)
# x.scrape_mostaghelat(path=path_mostaghelat_ghatee,
#                      report_type='ghatee', table_name='tblMostaghelatGhatee', append_to_prev=False)
# x.scrape_mostaghelat(path=path_mostaghelat_amade_ghatee,
#                      report_type='amade_ghatee', table_name='tblMostaghelatAmadeGhatee', append_to_prev=False)

tashkhis, ghatee, amade_ghatee, agg_most = final_most()
print('r')
agg_most['نام اداره سنتی'] = agg_most['نام اداره سنتی'].str.slice(0, 5)

lst_agg = [agg_most, agg_badvi_sanim, agg_tashkhis_ghatee_sanim, agg_tashkhis_saderNashode,
           agg_ghatee_saderNashode, agg_amade_ersal_beheiat, agg_tashkhis_eblagh_noGhatee]
# lst_agg = [agg_most, agg_badvi_sanim, agg_tashkhis_ghatee_sanim,
#            agg_tashkhis_saderNashode, agg_ghatee_saderNashode, agg_amade_ersal_beheiat]
merged_agg = ft.reduce(lambda left, right: pd.merge(
    left, right, how='outer', on='نام اداره سنتی'), lst_agg)
print('rr')
