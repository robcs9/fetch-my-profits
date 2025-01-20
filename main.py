import pandas as pd
import datetime as dt
from models.model import Operation
from utils import replaceDates, replaceQuantities, splitByMonths, readSheet

def main():
  sheet = readSheet('./carteira.csv')
  operations = Operation.buildOperations(sheet)
  # print(vars(operations[0]))
  # print([vars(op) for op in operations])
  shorts = []
  longs = []
  profits = 0
  losses = 0
  # Whenever an opposite type operation with the same ticker
  # is registered, calculate earnings and assign its consolidation status
  # 
  consolidations = []
  tickers = pd.unique(sheet['ticker'])
  groupedTickers = [el for el in sheet.groupby('ticker')][0]
  # how to turn this tuple into DataFrame?
  # df = pd.DataFrame(groupedTickers)
  # print(df)
  # print(f"date: {datetime.date.fromisoformat('2025-05-31') > datetime.date.fromisoformat('2025-05-31')}")
  
  # replace date string column with sortable date objects
  sheet = sheet.apply(replaceDates, axis=1)
  sheet = sheet.apply(replaceQuantities, axis=1)
  sortedByDate = sheet.sort_values(by='date')
  grouping = [el for el in sortedByDate.groupby(by='ticker')]
  
  # Format date back into local date string
  # datetime.date.strftime(date, "%d/%m/%Y")
  
  # calculate profits/losses
  # the first operation for each ticker should be treated with care
  # the subsequent operations will be used to perform the calculations on the first one
  
  # sample test - ALPA4
  ticker_ops = grouping[2][1]

  alpa4 = {
    'ops': ticker_ops,
    'initial': ticker_ops.iloc[0],
    'initial type': ticker_ops.iloc[0]['operation'], # type
    'initial total': ticker_ops.iloc[0]['total'],
    'owned quantity': 0,
    'owned total': 0,
  }
  
  
  # calculate monthly final quantity, profit and losses final result
  
  # monthly dates slicing (group operations per months as well before performing monthly calculations):
  # current_month, (for dates) current_month < (current_month + 1) % 12 (next month)
  #
  # reassign prices with proper sign based on the 'operation' column value
  
  # total = -quant * price
  # if init == 0:
  # diff0 = 2019 (ignore)
  # 
  # init = -2019
  # total_diff1 = -2019 + 2067 = -48
  # quant_diff1 = -300 + 300 = 0
  
  # situation
  # v - c
  # loss = 2019 - 2067 = -48
  # profit = 2019 - 2000 = 19
  # 
  # c - v
  # profit = 2000 - 2019 = -19
  # loss = 2019 - 2000 = 19
  #
  # if init_type == 'C': init - current
  # if init_type == 'V': -(init - current)
  
  
  # if next['operation'] != initial['operation']
  # calculation = initial['total'] - initial['operation'] if initial['operation'] == 'C' else next['total'] - initial['total']
  # reassessedQuantity = 
  # initial = 0; initial = initial - quantity if SELL else initial + quantity
  # calculate using yearly total shorts and longs (for taxes)
  # calculate monthly transactions value - double check stocks taxing rules (exempt)
  next = ticker_ops.iloc[1]['total']
  result = ticker_ops
  # result = ticker_ops.loc[ticker_ops['date'] > datetime.date.fromisoformat('2024-11-18')]
  result = ticker_ops.loc[ticker_ops['date'] > dt.date.fromisoformat('2024-11-01')]
  
  monthly_trades = splitByMonths(ticker_ops)
  
  # initial_op = oprts.iloc[0]
  # for i, op in enumerate(oprts):
  #   if i == 0:
  #     continue
  #   if op['type'] != initial_op['type'] and initial_op['type'] == 'C':
  #     # calc profit/loss
  #     result = initial_op['price'] - op['price']
  #     consolidated = True
  #     pass
  #   elif op['type'] != initial_op['type'] and initial_op['type'] == 'V':
  #     result = -initial_op['price'] + op['price']
  #     pass
  #   else:
  #     # process and store operation with previous ones
  #     pass
  
if __name__ == "__main__":
  main()