class Operation:
  result = "" # "Profit" or "Loss"
  
  def __init__(self, type, date, ticker, isConsolidated = False, price = 0, tax = 0):
    self.type = type # "Sell" or "Buy"
    self.price = price
    self.date = date
    self.ticker = ticker
    # self.trade_costs
    self.isConsolidated = isConsolidated
    self.tax = tax
    pass