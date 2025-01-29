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

def calcProfitLoss(rec: dict, tran: dict):
  if rec['type'] == 'V':
    diff = -(rec['avgPrice'] * abs(tran['units'])) + (tran['units']) * tran['price']
  else:
    diff = (rec['avgPrice'] * abs(tran['units'])) + (tran['units']) * tran['price']

  if diff <= 0:
    rec['profitlosses'].append(abs(diff))
  else:
    rec['profitlosses'].append(-abs(diff))
  return rec

def compareTransac(rec: dict, tran: dict): # rec, tran (record, transaction)
  rec['trades'].append(tran)
  rec['count'] += 1
  updated_units = rec['units'] + tran['units']

  if rec['units'] == 0:
    rec['profitlosses'].append(0)
    rec['avgPrice'] = tran['price']
    rec['units'] = tran['units']
    rec['type'] = tran['type']
    return rec
  
  if tran['type'] == rec['type']:
    rec['avgPrice'] = (rec['avgPrice'] + tran['price']) / 2
    rec['profitlosses'].append(0)
  else:
    # record changes and calculate profit/loss
    # updating units to match diff between the 2 transactions being compared to later calc the profit-loss
    # make a function that returns the dict which has the min between rec['units'] and tran['units'] so that you can properly perform the corrections to the price * units calculation before the calcProfitLoss is called
    
    if abs(tran['units']) <= abs(rec['units']):
      # rec['type'] won't change
      rec = calcProfitLoss(rec, tran)
    else:
      # rec['type'] flips
      # update units then calc profit/loss
      rec = calcProfitLoss(rec, tran)
      rec['type'] = 'C' if rec['type'] == 'V' else 'V'
  rec['units'] = updated_units
  return rec

# initial = {
#   'date': '2024-11-18', 'type': 'V', 'units': -300, 'price': 6.73, 'amount': -2019.0,
# }
# following = [
#   {'date': '2024-11-27','type': 'C', 'units': 300, 'price': 6.89, 'amount': 2067.0},
#   {'date': '2024-11-29','type': 'V', 'units': -200, 'price': 6.19, 'amount': -1238.0},
#   {'date': '2024-12-13','type': 'V', 'units': -200, 'price': 6.19, 'amount': -1238.0},
#   {'date': '2024-12-18','type': 'C', 'units': 400, 'price': 6.12, 'amount': 2448.0},
#   {'date': '2024-12-26','type': 'V', 'units': -400, 'price': 6.18, 'amount': -2472.0},
# ]

# Expected results:
# units flow: [-300, 0, -200, -400, 0, -400]
# profitlosses: [0, -48, 0, 0, 28, 0]

# record = {
#   'count': 1,
#   'trades': [initial.copy()],
#   'units': initial['units'],
#   'avgPrice': initial['price'],
#   'type': initial['type'],
#   'profitlosses': [0],
# }


# first comparison test
# second_transac = copy.deepcopy(following[0])
# second_transac = following[0].copy()
# record = compareTransac(record.copy(), second_transac)

# comparing transactions
# for trade in following:
#   next_tran = trade.copy()
#   record = compareTransac(record.copy(), next_tran)
# print(record)