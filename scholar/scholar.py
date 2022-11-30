from import_scholar import import_scholar

os, pd, maybe_make_dir, Scrape = import_scholar()

path = r'D:\projects\win_automation\saved_dir'
name = 'scholar'
path = os.path.join(path, name)
maybe_make_dir([path])
search_term = 'Swim: an exemplar for evaluation and comparison of self-adaptation approaches for web applications'

def run_scholar(done=False, headless=True, to_excel=True):
    global path
    x = Scrape()
    lst_cites = x.scrape_scholar(path=path, search_term=search_term)
    if to_excel:
        df = pd.DataFrame(lst_cites, columns=['Cites'])
        path = os.path.join(path,'swim.xlsx')
        df.to_excel(path)
        
    return lst_cites


lst_cites = run_scholar()
print('dd')
