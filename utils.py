import pandas as pd
import datetime as dt
from models.model import Operation

# def getTickerOps(sheet_df: pd.DataFrame, ticker: str):
  # return sheet_df[sheet_df['ticker'] == ticker]

def readSheet(filePath):
  sheet = pd.read_csv(filePath, encoding='utf-8')
  return sheet

def getTickerOps(oprts: list[Operation], ticker: str):
    ops = []
    for op in oprts:
      if op.ticker == ticker:
        ops.append(op)
    return ops

def groupTickerOps(oprts: list[Operation]):
  print(pd.unique([op.ticker for op in oprts])) #([op.ticker for op in oprts])
  print([op.ticker == ticker for op in oprts])
  return
  print([vars(el) for el in getTickerOps(oprts, 'MGLU3')])
  for ticker in oprts['ticker']:
    ops = getTickerOps(oprts)
  
def replaceDates(row):
  date = row['date'].split('/')
  date = dt.date(int(date[2]), int(date[1]), int(date[0]))
  row.loc['date'] = date
  return row

def replaceQuantities(row: pd.DataFrame):
  if row['operation'] == 'V':
    row['quantity'] *= -1
  return row

def splitByMonths(ops: pd.DataFrame):
    trades = []
    ops['date'] = pd.to_datetime(ops['date'])
    for month in range(1, 13):
      begin_mm = f'{month}' if month > 9 else f'0{month}'
      end_mm = f'{month+1}' if month + 1 > 9 else f'0{month+1}'
      
      begin_date = f'2024-{begin_mm}-01'
      end_date = f'2024-{end_mm}-01'
      if month == 12:
        end_date = f'2025-01-01'
      
      trades.append(ops.loc[(ops['date'] >= pd.to_datetime(begin_date)) & (ops['date'] < pd.to_datetime(end_date))])
    
    return pd.Series(trades)