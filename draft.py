import pandas as pd
from utils import readSheet, replaceDates, replaceQuantities, splitByMonths, compareTransac

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
  
def splitRecordsbyMonths(records: list[dict], calendar: dict = None):
  # 2024
  if calendar is None:
    calendar = {
      1:  [], 2:  [], 3:  [], 4:  [],
      5:  [], 6:  [], 7:  [], 8:  [],
      9:  [], 10: [], 11: [], 12: [],
    }
  for record in records:
    for i, trade in enumerate(record['trades']):
      trade['ticker'] = record['ticker']
      trade['profit'] = record['profitlosses'][i]
      calendar[trade['date'].month].append(trade)

  return calendar

def sumMonthlyPL(calendar: dict):
  calendar_sums = {
    1:  0, 2:  0, 3:  0, 4:  0,
    5:  0, 6:  0, 7:  0, 8:  0,
    9:  0, 10: 0, 11: 0, 12: 0,
  }
  for k in calendar:
    if len(calendar[k]) == 0:
      continue
    for transac in calendar[k]:
      calendar_sums[k] += transac['profit']
      
  return calendar_sums

def tickersMonthlyPL(calendar: dict):
  # tickers = pd.unique(sheet['ticker'])
  tickers_calendar = {
    1: {}, 2:  {}, 3:  {}, 4:  {},
    5: {}, 6:  {}, 7:  {}, 8:  {},
    9: {}, 10: {}, 11: {}, 12: {},
  }
  
  for k in calendar:
    if len(calendar[k]) == 0:
      continue
    for transac in calendar[k]:
      if tickers_calendar[k].get(transac['ticker']) is None:
        # tickers_calendar[k][transac['ticker']] = []
        tickers_calendar[k][transac['ticker']] = {
          'profit': 0,
          'loss': 0,
          'bought units': 0,
          'sold units': 0,
        }
      # tickers_calendar[k][transac['ticker']].append(transac['profit'])
      if transac['profit'] >= 0:
        tickers_calendar[k][transac['ticker']]['profit'] += transac['profit']
      else:
        tickers_calendar[k][transac['ticker']]['loss'] += transac['profit']

      if transac['units'] >= 0:
        tickers_calendar[k][transac['ticker']]['bought units'] += transac['units']
      else:
        tickers_calendar[k][transac['ticker']]['sold units'] += transac['units']
      
  return tickers_calendar

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

  year_trades = splitRecordsbyMonths(tickers_records)
  # print(year_trades)
  # testing sumRecordsResults

  yearly_pl = sumRecordsResults(tickers_records) # returns total monthly profits and losses
  # print(f'Year 2024\nProfits: {yearly_pl['p']}\nLosses: {yearly_pl['l']}')

  monthly_year_results = sumMonthlyPL(year_trades)
  results_df = pd.DataFrame({
    'Jan':  [monthly_year_results[1]],
    'Fev':  [monthly_year_results[2]],
    'Mar':  [monthly_year_results[3]],
    'Abr':  [monthly_year_results[4]],
    'Mai':  [monthly_year_results[5]],
    'Jun':  [monthly_year_results[6]],
    'Jul':  [monthly_year_results[7]],
    'Ago':  [monthly_year_results[8]],
    'Set':  [monthly_year_results[9]],
    'Out':  [monthly_year_results[10]],
    'Nov':  [monthly_year_results[11]],
    'Dez':  [monthly_year_results[12]],
  })
  results_df.to_csv('pl-results.csv')

  monthly_tickers_results = tickersMonthlyPL(year_trades)
  print(monthly_tickers_results)


if __name__ == '__main__':
  main()