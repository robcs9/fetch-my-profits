import numpy as np
import pandas as pd
import datetime as dt
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

def saveResults(results: dict):
  df_example = pd.DataFrame.from_dict({
    'Jan': [pd.DataFrame({'ticker': ['a','b']})],
    'Fev': [pd.DataFrame({'ticker': ['c','d']})],
    # 'Jan': {0: {'ticker': ['ABC'],'a': [1,2]}, 1: {'ticker': ['CDE'], 'a': [6,2]}},
    # 'Fev': {0: {'ticker': ['ABC'],'a': [1,2]}, 1: {'ticker': ['CDE'], 'a': [6,2]}},
  })
  # print(results[8]['ABEV3'])
  # print(df_example)

  months_cols = [
    'Jan', 'Fev', 'Mar',
    'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set',
    'Out', 'Nov', 'Dez'
  ]
  cols1 = ['Unidades Compradas', 'Unidades Vendidas', 'Lucro', 'Prejuizo']
  cols2 = ['Ticker', 'C/V', 'Unidades', 'Preço Medio', 'Lucro']
  
  calendar1_df = {
    'Mes': [],
    'Ticker': [],
    'Lucro': [],
    'Prejuizo': [],
    'Unidades Compradas': [],
    'Unidades Vendidas': [],
    'Total Lucro Mensal': [],
    'Total Prejuizo Mensal': [],
  }
  for month in results:
    if len(results[month]) == 0:
      continue
      
    # tickers = [ticker for ticker in results[month].values()]
    tickers = [ticker for ticker in results[month].items()]
    sum_profit = 0
    sum_loss = 0
    for i, ticker in enumerate(tickers):
      calendar1_df['Mes'].append(month)
      calendar1_df['Ticker'].append(ticker[0])
      calendar1_df['Lucro'].append(ticker[1]['profit'])
      calendar1_df['Prejuizo'].append(ticker[1]['loss'])
      calendar1_df['Unidades Compradas'].append(ticker[1]['bought units'])
      calendar1_df['Unidades Vendidas'].append(ticker[1]['sold units'])
      sum_profit += ticker[1]['profit']
      sum_loss += ticker[1]['loss']
      if (i == len(tickers) - 1):
        calendar1_df['Total Lucro Mensal'].append(sum_profit)
        calendar1_df['Total Prejuizo Mensal'].append(sum_loss)
        sum_profit = 0
        sum_loss = 0
      else:
        calendar1_df['Total Lucro Mensal'].append('')
        calendar1_df['Total Prejuizo Mensal'].append('')
  calendar1_df = pd.DataFrame(calendar1_df)
  calendar1_df['Unidades Vendidas'] = abs(calendar1_df['Unidades Vendidas'])
  # print([row for row in calendar1_df.groupby('Mes')])
  sorted_df = calendar1_df.sort_values(by='Mes')
  sorted_df.to_excel('resultados-trade2024.xlsx', index=False)
  print('resultados-trade2024.xlsx has been saved!')
  # index = {
  #   'Jan':  results[1], 'Fev':  results[2], 'Mar':  results[3],
  #   'Abr':  results[4], 'Mai':  results[5], 'Jun':  results[6],
  #   'Jul':  results[7], 'Ago':  results[8], 'Set':  results[9],
  #   'Out':  results[10], 'Nov':  results[11], 'Dez':  results[12],
  # }

def saveCSV(monthly_results: dict):
  results_df = pd.DataFrame({
    'Jan':  [monthly_results[1]],
    'Fev':  [monthly_results[2]],
    'Mar':  [monthly_results[3]],
    'Abr':  [monthly_results[4]],
    'Mai':  [monthly_results[5]],
    'Jun':  [monthly_results[6]],
    'Jul':  [monthly_results[7]],
    'Ago':  [monthly_results[8]],
    'Set':  [monthly_results[9]],
    'Out':  [monthly_results[10]],
    'Nov':  [monthly_results[11]],
    'Dez':  [monthly_results[12]],
  })
  # to-do: round-up decimals before saving
  results_df.to_csv('pl-results.csv')
  print('pl-results.csv has been saved!')

def saveTrades(records: list[dict]):
  data = {
    # 'Mes': [],
    'Data': [],
    'Ticker': [],
    'C/V': [],
    'Unidades': [],
    'Preço Medio': [],
    'Lucro': [],
  }
  for record in records:
    # print(record)
    for trade in record['trades']:
      data['Ticker'].append(record['ticker'])
      data['Data'].append(trade['date'])
      data['C/V'].append(trade['type'])
      data['Unidades'].append(trade['units'])
      data['Preço Medio'].append(trade['price'])
      data['Lucro'].append(trade['profit'])
  df = pd.DataFrame(data)
  df = df.sort_values(by=['Data', 'Ticker'])
  df.loc[:,'Data'] = df['Data'].apply(lambda e: e.strftime('%d/%m/%Y'))
  df.to_csv('operacoes-trade2024.csv', index=False)
  print('operacoes-trade2024.csv has been saved!')

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
  for ticker_op in grouping:
    # tickers.append(ticker_op)
    record, following_trades = buildRecord(ticker_op[1].copy())
    for trade in following_trades:
      record = compareTransac(record, trade)
    tickers_records.append(record)

  year_trades = splitRecordsbyMonths(tickers_records)
  
  # yearly_pl = sumRecordsResults(tickers_records) # returns total monthly profits and losses
  # print(f'Year 2024\nProfits: {yearly_pl['p']}\nLosses: {yearly_pl['l']}')

  monthly_year_results = sumMonthlyPL(year_trades)
  saveCSV(monthly_year_results)

  monthly_tickers_results = tickersMonthlyPL(year_trades)
  saveResults(monthly_tickers_results)
  saveTrades(tickers_records)
if __name__ == '__main__':
  main()