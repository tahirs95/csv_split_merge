import pandas as pd
import math

df1 = pd.read_csv('split_1.csv')
length = len(df1.columns)


df_list = [df1, df2, df3]

for df in df_list:
    if len(df.columns) != length:
        break
    else:
        pass

df2 = pd.read_csv('split_2.csv')
len(df2.columns)

df3 = pd.read_csv('split_3.csv')
len(df3.columns)

new_df = pd.concat(pdList)

# data = header.append(df, ignore_index=True)
new_df.to_csv("merged.csv", header=True, index=None)

