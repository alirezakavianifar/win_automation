import pandas as pd
from import_scholar import import_scholar

os, pd, maybe_make_dir, Scrape = import_scholar()

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


def get_year(cite):
    for i in years:
        if i in cite:
            return i


def get_type(cite):
    for i in article_types:
        if i in cite:
            return i

    return 'possible journal'


def run_scholar(done=False, headless=True, to_excel=True):
    global path
    x = Scrape()
    lst_cites, lst_links = x.scrape_scholar(path=path, search_term=search_term)
    if to_excel:
        df = pd.DataFrame({'Cites': lst_cites, 'Links': lst_links})
        df['year'] = df['Cites'].apply(get_year)
        df['type'] = df['Cites'].apply(get_type)
        path = os.path.join(path, 'Deltaiot.xlsx')
        df.to_excel(path, index=False)

        df_journal = df.loc[df['type'] == 'journal']


# df = run_scholar()
df = pd.read_excel(
    r'D:\projects\win_automation\saved_dir\scholar\Deltaiot.xlsx')
df_journals = df['links'].loc[df['type'] == 'Journal'].values.tolist()

x = Scrape()
for item in df_journals[:2]:
    x.scrape_scihub(path=path, search_term=item)
