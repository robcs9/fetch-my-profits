import pandas

class Operation:
  result = '' # "Profit" or "Loss"
  
  def __init__(self, type='C/V', date='dd/mm/aaaa', ticker='TICK3R', quantity=0, price = 0, tax = 0, isConsolidated = False):
    self.type = type # "Sell" or "Buy"
    self.price = price
    self.date = date
    self.ticker = ticker
    # self.trade_costs
    self.isConsolidated = isConsolidated
    self.tax = tax
    self.quantity = quantity
    self.total = self.quantity * self.price
    # self.name = ""
  
  @staticmethod
  def buildOperations(sheet: pandas.DataFrame):
    ops_count = sheet.count(axis=0).iloc[0]
    operations = []
    for i in range(ops_count):

      op = Operation(
        date=sheet.iloc[i]['date'],
        ticker=sheet.iloc[i]['ticker'],
        type=sheet.iloc[i]['operation'],
        price=sheet.iloc[i]['price'],
        quantity=int(sheet.iloc[i]['quantity']),
      )
      operations.append(op)
    return operations
