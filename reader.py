import pandas as pd

df = pd.read_csv('./train.csv')
df.sort(columns=['Device', 'T'], inplace=True)
devices = df['Device'].unique()
print devices
