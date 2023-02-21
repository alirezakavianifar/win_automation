from scholar import run_scholar, get_pdf_files
import pandas as pd

article_types = ['Conference', 'Symposium',
                 'Workshop', 'Journal']

if __name__ == '__main__':
    
    path = run_scholar(headless=False, to_excel=True, download_pdf=True)
    
    df_scholar = pd.read_excel(path)
    
    df_final = get_pdf_files(df_scholar)
    
    print('r')
