import pandas as pd


# df = pd.read_excel(r'D:\projects\data\iris\tashkhisEblaghShode.xlsx', chunksize=11)

# df.to_csv(r'D:\projects\data\iris\tashkhisEblaghShode.csv')

df = pd.read_csv(r'D:\projects\data\iris\tashkhisEblaghShode.csv', chunksize=10)

len(df)