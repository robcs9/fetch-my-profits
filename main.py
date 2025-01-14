import pandas
from models.model import Operation

def readSheet(filePath):
  return pandas.read_csv(filePath, encoding='utf-8')
def main():
  sheet = readSheet('./carteira.csv')
  oprts = sheet[sheet['ticker'] == 'MGLU3']
  # 
  initial_op = oprts.iloc[0]
  for i, op in enumerate(oprts):
    if i == 0:
      continue
    if op['type'] != initial_op['type'] and initial_op['type'] == 'C':
      # calc profit/loss
      result = initial_op['price'] - op['price']
      pass
    elif op['type'] != initial_op['type'] and initial_op['type'] == 'V':
      result = -initial_op['price'] + op['price']
      pass
    else:
      # process and store operation with previous ones
      pass
  
if __name__ == "__main__":
  main()