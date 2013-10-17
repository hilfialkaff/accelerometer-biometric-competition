import pandas as pd

df = pd.read_csv('./data/train.csv')
df.sort(columns=['Device', 'T'], inplace=True)
devices = df['Device'].unique()
print devices
