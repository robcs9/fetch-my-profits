import pandas
from models.model import Operation

# def getTickerOps(sheet_df: pandas.DataFrame, ticker: str):
  # return sheet_df[sheet_df['ticker'] == ticker]

def readSheet(filePath):
  sheet = pandas.read_csv(filePath, encoding='utf-8')
  return sheet

def main():
  sheet = readSheet('./carteira.csv')
  operations = Operation.buildOperations(sheet)
  # print(vars(operations[0]))
  # print([vars(op) for op in operations])
  
  consolidations = []
  oprts = sheet[sheet['ticker'] == 'MGLU3']
  # oprts = getTickerOps(sheet,'MGLU3')
  
  def getTickerOps(oprts: list[Operation], ticker: str):
    ops = []
    for op in oprts:
      if op.ticker == ticker:
        ops.append(op)
    return ops
  
  print([vars(el) for el in getTickerOps(operations, 'MGLU3')])
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