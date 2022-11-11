from helpers import get_mashaghelsonati, get_tblreports_date, connect_to_sql
from constants import get_table_names, geck_location
from sql_queries import sql_delete, create_sql_table, insert_into

saved_folder = geck_location(set_save_dir=True)
eblagh = False
date = 140106


def get_tashkhis_ghatee_sonati(date=date, eblagh=eblagh, saved_folder=saved_folder):
    #
    if eblagh == False:
        amade_ersal_beheiat = get_mashaghelsonati(
            'heiat', date=date, eblagh=eblagh)
        tashkhis_saderNashode = get_mashaghelsonati(
            'tashkhis', date=date, eblagh=eblagh)
        ghatee_saderNashode = get_mashaghelsonati(
            'ghatee', date=date, eblagh=eblagh)
        tashkhis_saderNashode.to_excel(
            '%s/mashaghelSonati_noeblagh_t.xlsx' % saved_folder)
        ghatee_saderNashode.to_excel(
            '%s/mashaghelSonati_noeblagh_g.xlsx' % saved_folder)
        amade_ersal_beheiat.to_excel(
            '%s/mashaghelSonati_amadeersalbeheiat.xlsx' % saved_folder)
        return tashkhis_saderNashode, ghatee_saderNashode, amade_ersal_beheiat

    else:

        tashkhis_sadere, tashkhis_eblaghi = get_mashaghelsonati(
            'tashkhis', date=date, eblagh=eblagh)
        ghatee_sadere, ghatee_eblaghi = get_mashaghelsonati(
            'ghatee', date=date, eblagh=eblagh)
        tashkhis_sadere.to_excel(
            '%s/mashaghelSonati_tashkhisSadere.xlsx' % saved_folder)
        ghatee_sadere.to_excel(
            '%s/mashaghelSonati_ghateeSadere.xlsx' % saved_folder)
        tashkhis_eblaghi.to_excel(
            '%s/mashaghelSonati_tashkhisEblaghi.xlsx' % saved_folder)
        ghatee_eblaghi.to_excel(
            '%s/mashaghelSonati_ghateeEblaghi.xlsx' % saved_folder)
        return tashkhis_sadere, ghatee_sadere, tashkhis_eblaghi, ghatee_eblaghi


def dump_to_sql():

    table_names = [
        ('tblMashaghelSonatiTashkhisSadere', tashkhis_sadere),
        ('tblMashaghelSonatiTashkhisEblaghi', tashkhis_eblaghi),
        ('tblMashaghelSonatiGhateeSadere', ghatee_sadere),
        ('tblMashaghelSonatiGhateeEblaghi', ghatee_eblaghi)
    ]

    for item in table_names:

        sql_delete_query = sql_delete(item[0])
        connect_to_sql(sql_query=sql_delete_query,
                       connect_type='dropping sql table')

        sql_create_table_query = create_sql_table(item[0], item[1].columns)
        connect_to_sql(sql_create_table_query,
                       connect_type='creating sql table')

        sql_insert = insert_into(item[0], item[1].columns)
        connect_to_sql(sql_query=sql_insert, df_values=item[1].values.tolist(
        ), connect_type='inserting into sql table')
