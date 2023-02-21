def import_scholar():
    import pandas as pd
    import numpy as np
    import sys
    import glob
    sys.path.append(r'D:\projects\win_automation')
    sys.path.append(r'D:\projects\win_automation\tgju\tkinter')
    from scrape import Scrape
    from helpers import maybe_make_dir
    import os
    import PyPDF2
    return os, np, PyPDF2, glob, pd, maybe_make_dir, Scrape
