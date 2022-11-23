def import_tgju():
    import sys
    sys.path.append(r'D:\projects\win_automation')
    sys.path.append(r'D:\projects\win_automation\tgju\tkinter')
    from tgju_tkinter_constants import get_shared_var
    import pandas as pd
    from scrape import Scrape
    from helpers import maybe_make_dir, get_update_date, drop_into_db
    from constants import get_sql_con
    import time
    import datetime
    from aspect_tgju import log, internet_on, done_log, run_tgju_log

    return sys, pd, Scrape, maybe_make_dir, get_update_date, drop_into_db, get_sql_con, time, datetime, log, internet_on, done_log, run_tgju_log, get_shared_var
