import pandas as pd

months = ['jan', 'fev', 'mar']
cols = ['initial', 'age']
idx = ['Will', 'Torres', 'Torres']
ages = [12, 15]
data = [
  ('W', 12, 'W', 13, 'W', 14),
  ('T', 12, '', '', 'W', 14),
  ('T', 12, 'W', 13, None, None),
]
multi_col = pd.MultiIndex.from_tuples([(x,y) for x in months for y in cols])
df = pd.DataFrame(data, columns=multi_col)
print(df)
# print([d for d in df.groupby(by=('jan','initial'))])