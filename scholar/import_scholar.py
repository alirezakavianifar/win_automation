def import_scholar():
    import pandas as pd
    import sys
    sys.path.append(r'D:\projects\win_automation')
    sys.path.append(r'D:\projects\win_automation\tgju\tkinter')
    from scrape import Scrape
    from helpers import maybe_make_dir
    import os
    return os, pd, maybe_make_dir, Scrape
