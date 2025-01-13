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
    if op['type'] != initial_op['type']:
      # calc profit/loss
      pass
    else:
      # process and store operation with previous ones
      pass
  
if __name__ == "__main__":
  main()