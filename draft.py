# import copy

import pandas as pd
from utils import readSheet, replaceDates, replaceQuantities, splitByMonths, compareTransac

# builds record of a given period of trades
def buildRecord(ticker_trades: pd.DataFrame):
  # ticker_trades = ticker_trades.rename(columns={'operation': 'type'})
  if len(ticker_trades) < 1:
    print('Found no trades to be processed')
    return None
  trades = [
    {
      'date': trade[1]['date'],
      'type': trade[1]['operation'],
      'units': trade[1]['quantity'],
      'price': trade[1]['price'],
      'amount': trade[1]['price'] * trade[1]['quantity'],
    } for trade in ticker_trades.iterrows()
  ]
  initial = trades[0]
  following_trades = trades[1:]

  record = {
    'ticker': ticker_trades.iloc[0]['ticker'],
    'count': 1,
    'trades': [initial.copy()],
    'units': initial['units'],
    'avgPrice': initial['price'],
    'type': initial['type'],
    'profitlosses': [0],
  }

  return record, following_trades

def sumRecordsResults(records: list[dict]):
  profit = 0
  loss = 0
  for rec in records:
    for pl in rec['profitlosses']:
      if pl >= 0:
        profit += pl
      else:
        loss += pl
  return {'p': profit, 'l': loss}
  

# Rewrite function to support records
def splitTradesByMonths(ops: pd.DataFrame):
  return
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
  
def main():
  # to-do: handle all months by year to avoid mix ups
  sheet = readSheet('./carteira2024.csv')
  # tickers = pd.unique(sheet['ticker'])
  # groupedTickers = [el for el in sheet.groupby('ticker')][0]
  
  sheet = sheet.apply(replaceDates, axis=1)
  sheet = sheet.apply(replaceQuantities, axis=1)
  sortedByDate = sheet.sort_values(by='date')
  grouping = [el for el in sortedByDate.groupby(by='ticker')]

  tickers_records = []
  # tickers = []
  for ticker_op in grouping:
    # tickers.append(ticker_op)
    record, following_trades = buildRecord(ticker_op[1].copy())
    for trade in following_trades:
      record = compareTransac(record, trade)
    tickers_records.append(record)

  year_trades = splitTradesByMonths(tickers_records)
  # testing sumRecordsResults
  sum = sumRecordsResults(tickers_records) # returns total monthly profits and losses
  print(sum)
  # remember to actually call the function for each separate months instead once splitTradesByMonths is rewritten
  # eventually, leading to calling sumRecordsResults(splitTradesByMonths(records))


  """ 
  # sample test - ALPA4 November results
  ticker_ops = grouping[2][1]
  alpa4_monthly_trades = splitByMonths(ticker_ops)
  alpa4_nov = alpa4_monthly_trades[10]
  # initial = last_month_rec attrs (prev_month_trades[-1], units, avgPrice, type) if rec['units'] != 0 else transactions[0]
  # initial record data => first transaction in the current month or the remaining last one carried from the previous one
  record, following_trades = buildRecord(alpa4_nov.copy()) # pass monthly ticker trades? (alpa4_monthly_trades) in this case
  if len(following_trades) == 0:
    print('No trades available to process for the month 11')
    # return record
  
  # comparing transactions
  for trade in following_trades:
    next_tran = trade.copy()
    record = compareTransac(record.copy(), next_tran)
  """


if __name__ == '__main__':
  main()