from scrape import Scrape
from helpers import maybe_make_dir

path = r'H:\پروژه اتوماسیون گزارشات\monthly_reports\saved_dir\tgju'

maybe_make_dir([path])

x = Scrape()

x.scrape_tgju(path=path)
