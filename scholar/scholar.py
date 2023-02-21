from functools import reduce
import pandas as pd
from import_scholar import import_scholar

os, np, PyPDF2, glob, pd, maybe_make_dir, Scrape = import_scholar()

path = r'D:\projects\win_automation\saved_dir'
name = 'scholar'
path = os.path.join(path, name)
maybe_make_dir([path])
search_term = 'Deltaiot: A self-adaptive internet of things exemplar'
years = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014',
         '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005',
         '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996',
         '1995', '1994', '1993', '1992']
article_types = ['Conference', 'Symposium',
                 'Workshop', 'Journal', 'dissertation', 'arXiv']

# helper methods


def get_year(cite):
    for i in years:
        if i in cite:
            return i


def get_type(cite):
    for i in article_types:
        if i in cite:
            return i
    return 'possible journal'


def run_scholar(done=False, headless=True, to_excel=True, file_name='Deltaiot.xlsx', download_pdf=False):
    global path
    x = Scrape()
    lst_cites, lst_links, lst_pdf = x.scrape_scholar(path=path, search_term=search_term, download_pdf=download_pdf)
    if to_excel:
        df = pd.DataFrame({'Cites': lst_cites, 'Links': lst_links})
        df['year'] = df['Cites'].apply(get_year)
        df['type'] = df['Cites'].apply(get_type)
        path = os.path.join(path, file_name)
        df.to_excel(path, index=False)
        return path
    else:
        return df


def get_pdf_files(df=None):
    lst_success = []
    x = Scrape()
    lst_journals = df['Links'].loc[(
        df['type'] in article_types[:4])].values.tolist()

    # Get files from scihub
    def get_from_scihub():
        for item in lst_journals:
            try:
                lst_success.append(x.scrape_scihub(
                    path=path, search_term=item))
            except:
                continue

    def check_if_downloaded():
        df_success = pd.DataFrame(
            {'links': lst_journals, 'pdf_available': lst_success})
        df_merge = df.merge(df_success, how='left',
                            left_on='links', right_on='links')
        return df_merge

    def get_from_scholar(df_merge=None):
        nonlocal lst_success
        lst_success = []
        df_remaining = df_merge[df_merge['pdf_available'] == 'failure']

        lst_success.extend(x.scrape_scholar(
            path=path, search_term=df_remaining['Cites'].iloc[0], download_pdf=True, files=df_remaining))
        df_remaining['pdf_available'] = lst_success
        return df_remaining

    get_from_scihub()
    df_merge = check_if_downloaded()

    df_remaining = get_from_scholar(df_merge)
    df_success = df_merge[df_merge['pdf_available'] != 'failure']
    df_merge_final = df_success.merge(df_remaining, how='left',
                                      left_on='links', right_on='links')

    return df_merge_final
    # check which files were successfully downloaded

    # Get the remaining files from google scholar

    # return lst_success


# get_pdf_files()


# name = os.path.join(path, 'merged.xlsx')
# df_merge.to_excel(name)


# lst_merged = glob.glob(path + "/merged*" + '.xlsx')

# lst_m = [pd.read_excel(file) for file in lst_merged]

# df_merged_all = reduce(lambda left, right: pd.merge(left, right, on=['links'],
#                                                     how='outer'), lst_m)

# df_merged_all.to_excel(
#     r'D:\projects\win_automation\saved_dir\scholar\final.xlsx')
# df_final = pd.read_excel(
#     r'D:\projects\win_automation\saved_dir\scholar\df_final.xlsx')
# df_final['pdf_available1'].fillna(df_final['pdf_available4'], inplace=True)
# df_final.to_excel(
#     r'D:\projects\win_automation\saved_dir\scholar\df_final.xlsx', index=False)


def count_serach_term(term):
    pdffiles = glob.glob(path + "/*" + '.pdf')
    for pdffile in pdffiles:
        i = 0
        reader = PyPDF2.PdfFileReader(pdffile)
        for page_number in range(0, reader.numPages):
            page = reader.getPage(page_number)
            page_content = page.extractText()
            if term in page_content:
                i += 1
        print('%s: %s' % (pdffile, i))
