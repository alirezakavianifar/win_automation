import xlrd
import pandas as pd
from helpers import drop_into_db, merge_multiple_excel_files

# r'E:\automating_reports_V2\saved_dir\codeghtesadi\codeeghtesadi.csv', chunksize=10)

# for item in df:
#     df1 = item
#     break

# df.to_csv(r'E:\automating_reports_V2\saved_dir\codeghtesadi\codeeghtesadi.csv')


# drop_into_db('tblCodeeghtesadi', df1.columns.tolist(), df1.values.tolist())
path = r'E:\automating_reports_V2\saved_dir\mostaghelat\mostaghelat_ghatee'

df = merge_multiple_excel_files(
    path, path, table_name='tblMostaghelatTashkhis', delete_after_merge=True, postfix='xls', drop_to_sql=True)


# df = xlrd.open_workbook(
#     r'E:\automating_reports_V2\saved_dir\mostaghelat\mostaghelat_ghatee\Rpt_Deterministic(18).xls')

# df = pd.read_excel(
#     r'E:\automating_reports_V2\saved_dir\mostaghelat\mostaghelat_ghatee\Rpt_Deterministic(18).xls')
# df = pd.read_excel(
#     r'E:\automating_reports_V2\saved_dir\mostaghelat\mostaghelat_ghatee\Rpt_Deterministic(19).xls')
