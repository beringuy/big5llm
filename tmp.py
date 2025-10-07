
import pandas as pd

df = pd.read_csv("ipip50.csv")
df

df.loc[0]
df.iloc[0]
df[df.columns.tolist()[1 + 0]]