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
    'count': 1,
    'trades': [initial.copy()],
    'units': initial['units'],
    'avgPrice': initial['price'],
    'type': initial['type'],
    'profitlosses': [0],
  }

  return record, following_trades


def main():
  sheet = readSheet('./carteira.csv')
  # tickers = pd.unique(sheet['ticker'])
  # groupedTickers = [el for el in sheet.groupby('ticker')][0]
  
  # replace date string column with sortable date objects
  sheet = sheet.apply(replaceDates, axis=1)
  sheet = sheet.apply(replaceQuantities, axis=1)
  sortedByDate = sheet.sort_values(by='date')
  grouping = [el for el in sortedByDate.groupby(by='ticker')]
  
  # sample test - ALPA4 November results
  ticker_ops = grouping[2][1]
  alpa4_monthly_trades = splitByMonths(ticker_ops)
  alpa4_nov = alpa4_monthly_trades[10]

  # initial = last_month_rec attrs (prev_month_trades[-1], units, avgPrice, type) if rec['units'] != 0 else transactions[0]
  # initial record data => first transaction in the current month or the remaining last one carried from the previous one
  record, following_trades = buildRecord(alpa4_nov.copy()) # pass monthly ticker trades? (alpa4_monthly_trades) in this case
  if len(following_trades) == 0:
    print('No trades available to process for the month 11')
    return record
  
  # comparing transactions
  for trade in following_trades:
    next_tran = trade.copy()
    record = compareTransac(record.copy(), next_tran)
  
if __name__ == '__main__':
  main()