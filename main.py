import pandas as pd
import datetime as dt
from models.model import Operation
from utils import replaceDates, replaceQuantities, splitByMonths, readSheet
from utils import compareTransac
import math

def main():
  sheet = readSheet('./carteira.csv')
  shorts = []
  longs = []
  # Whenever an opposite type operation with the same ticker
  # is registered, calculate earnings and assign its consolidation status
  # 
  
  # consolidations = []
  # tickers = pd.unique(sheet['ticker'])
  # groupedTickers = [el for el in sheet.groupby('ticker')][0]
  
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
  # calculate monthly final quantity, profit and losses final result
  
  # monthly dates slicing (group operations per months as well before performing monthly calculations):
  # current_month, (for dates) current_month < (current_month + 1) % 12 (next month)
  #
  # reassign prices with proper sign based on the 'operation' column value
  
  
  alpa4 = {
    'ops': ticker_ops,
    # 'initial': ticker_ops.iloc[0],
    'owned': ticker_ops.iloc[0],
    # 'initial type': ticker_ops.iloc[0]['operation'], # type
    # 'initial total': ticker_ops.iloc[0]['total'],
    'owned type': ticker_ops.iloc[0]['operation'],
    'owned quantity': ticker_ops.iloc[0]['quantity'],
    'owned total': ticker_ops.iloc[0]['price'] * ticker_ops.iloc[0]['quantity'],
  }
  
  alpa4_monthly_trades = splitByMonths(ticker_ops)
  nov = alpa4_monthly_trades[11]
  nov.loc[:,'total'] = nov['price'] * nov['quantity']
  initial_nov = nov.iloc[0]
  next_trades = nov.iloc[1:]
  if len(next_trades) == 0:
    print('No trades left to process for the month 11')
    return None

  profits = []
  losses = []
  # total_values = next_trades['price'] * next_trades['quantity']
  for idx, nxt in next_trades.iterrows():
    liquidated = False
    prev_quant = alpa4['owned quantity']
    prev_total = alpa4['owned total']
    profit = 0
    loss = 0
    sum = alpa4['owned total'] + nxt['total']
    liquidating = 0
    if abs(nxt['quantity']) >= abs(alpa4['owned quantity']):
      liquidating = alpa4['owned']['price'] * abs(nxt['quantity'])
      alpa4['owned type'] = 'V'
    else:
      liquidating = alpa4['owned quantity']
    reversing_quantity = sum
    alpa4['owned quantity'] += nxt['quantity']
    # alpa4['owned total'] = ...
    # curr_quant = nxt['quantity']
    # new_quant = prev_quant + curr_quant
    # alpa4['owned'] = nxt # latest trade processed
    
    
    # register increase in owned shares
    # if new_quant > prev_quant and alpa4['owned type'] == 'C':
    if nxt['operation'] != alpa4['owned type']:
      liquidated = True
      profit = -sum
      if alpa4['owned type'] == 'C' and profit >= 0:
        profits.append(profit)
        alpa4['owned total'] = 0
      else:
        pass
    if alpa4['owned quantity'] >= 0 and alpa4['owned type'] == 'C':
      pass
    # alpa4['owned quantity'] += nxt['quantity']
    # alpa4['owned total'] += nxt['total']

      

    # register profit or loss
    # elif new_quant >= 0 and alpa4['owned type'] == 'C':
      
    # register profit or loss and invert position if < 0
    # elif new_quant <= 0 and alpa4['owned type'] == 'C':
      # pass
    # register increase in owned shares
    # if new_quant < prev_quant and alpa4['owned type'] == 'V':
      # pass
    # if new_quant >= 0 and alpa4['owned type'] == 'V':
      # pass
    # if new_quant > prev_quant and alpa4['owned type'] == 'V':
      # pass
    # if nxt['operation'] != alpa4['owned type']:
      # nxt_total = nxt['price'] * nxt['quantity']
      # liquidated_total = alpa4['owned total'] + nxt_total
      # liquidated_quantity = alpa4['owned quantity'] + nxt['quantity']
      # liquidated = True

    #if new quant value is greater than initial... or if it's lower... or if it's 0...
    # if liquidated and alpa4['owned type'] == 'C':
    # elif liquidated and alpa4['owned type'] == 'V':
        
    # if quantity/total sign(s) changed, ...
    # if quantity/total become 0, ...
    # if none of the above changes, ...

  # if next['operation'] != initial['operation']
  # calculation = initial['total'] - initial['operation'] if initial['operation'] == 'C' else next['total'] - initial['total']
  # reassessedQuantity = 
  # initial = 0; initial = initial - quantity if SELL else initial + quantity
  # calculate using yearly total shorts and longs (for taxes)
  # calculate monthly transactions value - double check stocks taxing rules (exempt)
  
  
if __name__ == "__main__":
  main()