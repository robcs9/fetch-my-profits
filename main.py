import pandas as pd
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
  sortedByDate = sheet.sort_values(by='date')
  grouping = [el for el in sortedByDate.groupby(by='ticker')]
  print(grouping[6])
  # sorting by date (string) doesn't work as is
  
  # building date objects
  import datetime
  print(f"date: {datetime.date.fromisoformat('2025-05-31')}")
  
  # replace date string column with sortable date objects
  
  # sorting by date objects column
  
  # groupTickerOps(operations)
  
  return

  # oprts = sheet[sheet['ticker'] == 'MGLU3']
  # oprts = getTickerOps(sheet,'MGLU3')
  
  # print([vars(el) for el in getTickerOps(operations, 'MGLU3')])
  # 
  
  initial_op = oprts.iloc[0]
  for i, op in enumerate(oprts):
    if i == 0:
      continue
    if op['type'] != initial_op['type'] and initial_op['type'] == 'C':
      # calc profit/loss
      result = initial_op['price'] - op['price']
      consolidated = True
      pass
    elif op['type'] != initial_op['type'] and initial_op['type'] == 'V':
      result = -initial_op['price'] + op['price']
      pass
    else:
      # process and store operation with previous ones
      pass
  
if __name__ == "__main__":
  main()