def import_nobatdotir():
    import sys
    sys.path.append(r'D:\projects\win_automation')
    sys.path.append(r'D:\projects\win_automation\tgju\tkinter')
    import pandas as pd
    from scrape import Scrape
    from helpers import maybe_make_dir, get_update_date, drop_into_db
    from constants import get_sql_con
    import time
    import datetime

    return sys, pd, Scrape, maybe_make_dir, get_update_date, drop_into_db, get_sql_con, time, datetime
