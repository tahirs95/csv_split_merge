import pandas as pd
import math

df = pd.read_csv('cluster.csv')

files = 3
header_rows = 3
size = 200
if files:
    size = math.ceil(len(df)/files)
list_of_dfs = [df.loc[i:i+size-1,:] for i in range(0, len(df),size)]
if header_rows == 1:
    for i, df in enumerate(list_of_dfs):
        df.to_csv("split_{}.csv".format(i+1), header=True, index=None)
else:
    header = df.iloc[0:header_rows-1]
    for i, df in enumerate(list_of_dfs):
        data = header.append(df, ignore_index=True)
        data.to_csv("split_{}.csv".format(i+1), header=True, index=None)

