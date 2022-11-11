from helpers import drop_into_db
import pandas as pd

df = pd.read_csv(
    r'E:\automating_reports_V2\saved_dir\codeghtesadi\codeeghtesadi.csv', chunksize=10)

for item in df:
    df1 = item
    break

# df.to_csv(r'E:\automating_reports_V2\saved_dir\codeghtesadi\codeeghtesadi.csv')


drop_into_db('tblCodeeghtesadi', df1.columns.tolist(), df1.values.tolist())
