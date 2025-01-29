import copy

# p = price, v = value, q = quant

initial = {
  'date': '2024-11-18', 'type': 'V', 'units': -300, 'price': 6.73, 'amount': -2019.0,
}
following = [
  {'date': '2024-11-27','type': 'C', 'units': 300, 'price': 6.89, 'amount': 2067.0},
  {'date': '2024-11-29','type': 'V', 'units': -200, 'price': 6.19, 'amount': -1238.0},
  {'date': '2024-12-13','type': 'V', 'units': -200, 'price': 6.19, 'amount': -1238.0},
  {'date': '2024-12-18','type': 'C', 'units': 400, 'price': 6.12, 'amount': 2448.0},
  {'date': '2024-12-26','type': 'V', 'units': -400, 'price': 6.18, 'amount': -2472.0},
]
record = {
  'count': 1,
  'trades': [initial.copy()],
  'units': initial['units'],
  'avgPrice': initial['price'],
  'type': initial['type'],
  # 'amount': initial['amount'],
  # 'profits': [0],
  # 'losses': [],
  'profitlosses': [0],
}

def calcAvgPrice(trades: list):
  # avgprice based on current owned shares price and the new trade being added
  # (currPrice + newPrice) / 2 ? 
  # 
  sum = 0
  for t in trades:
    sum += t['price']
  return sum / len(trades)

def calcProfitLoss(rec: dict, tran: dict):
  # diff = (rec['avgPrice'] * abs(tran['units'])) + tran['price'] * tran['units']
  if rec['type'] == 'V':
    diff = -(rec['avgPrice'] * abs(tran['units'])) + (tran['units']) * tran['price']
  else:
    diff = (rec['avgPrice'] * abs(tran['units'])) + (tran['units']) * tran['price']

  # if diff <= 0:
  #   rec['profits'].append(abs(diff))
  # if diff > 0:
  #   rec['losses'].append(-abs(diff))
  if diff <= 0:
    rec['profitlosses'].append(abs(diff))
  else:
    rec['profitlosses'].append(-abs(diff))
  return rec
  # 1000 + -1100 = -100 (C profit)
  # -1000 + 900 = -100 (V profit)
  # 1000 + -900 = 100 (C loss)
  # -1000 + 1100 = 100 (V loss)
  # -1000 + 1000 = 0
  # 1000 + -1000 = 0
  

def compareTransac(rec: dict, tran: dict): # rec, tran => record, transaction
  rec['trades'].append(tran)
  rec['count'] += 1
  updated_units = rec['units'] + tran['units']

  if rec['units'] == 0:
    rec['profitlosses'].append(0)
    rec['avgPrice'] = tran['price']
    rec['units'] = tran['units']
    rec['type'] = tran['type']
    return rec
  
  if tran['type'] == rec['type']:
    # rec['units'] = rec['units'] + tran['units']
    rec['avgPrice'] = (rec['avgPrice'] + tran['price']) / 2
    rec['profitlosses'].append(0)
    # rec['amount'] = rec['amount'] + tran['amount']
  else:
    # record changes and calculate profit/loss
    # units update: # prioritize the rule min(abs(rec['units']),abs(tran['units'])) for the following operations
    # 20 + -100 = -80; calcProfitLoss between (20 * avgPrice) and (-20 * tran['price']); updated_units = -80; corrected tran price
    # -20 + 100 = 80; calcProfitLoss between (-20 * avgPrice) and (20 * tran['price']); updated_units = 80; corrected tran price
    # 100 + -20 = 80; calcProfitLoss between (20 * avgPrice) and (-20 * tran['price']); updated_units = 80; corrected rec price
    # -100 + 20 = -80; calcProfitLoss between (-20 * avgPrice) and (20 * tran['price']); updated_units = -80; corrected rec price
    # apply price correction with rec['units'] and tran['price'] or tran['units'] and rec['avgPrice'] before calling calcProfitLoss

    # pairs = [[-100,-20],[20,100],[-100,20],[-20,100]]
    # print(min(abs(-100),abs(20)) % abs(-20) == 0)
    # print(min(abs(-100),abs(20)) % abs(-20) == 0 for x,y in pairs)
    # print([min(abs(x),abs(y)) for x,y in pairs])
    
    # updating units to match diff between the 2 transactions being compared to later calc the profit-loss
    # make a function that returns the dict which has the min between rec['units'] and tran['units'] so that you can properly perform the corrections to the price * units calculation before the calcProfitLoss is called
    # actual_units = min(abs(rec['units']),abs(tran['units'])) * sign
    # abs(???['units']) % min(abs(rec['units']),abs(tran['units'])) == 0
    # calcProfitLoss(x,y)
    
    if abs(tran['units']) <= abs(rec['units']):
      # rec['type'] won't change
      rec = calcProfitLoss(rec, tran)
    # elif tran['units'] > rec['units']:
    else:
      # rec['type'] flips
      # update units then calc profit/loss
      # min(abs(rec['units']),abs(tran['units'])) * sign
      # updated_units = tran['units'] if min(abs(rec['units']),abs(tran['units']))
      rec = calcProfitLoss(rec, tran)
      # rec['units'] = rec['units'] + tran['units']
      rec['type'] = 'C' if rec['type'] == 'V' else 'V'
  rec['units'] = updated_units
  return rec

# comparing transactions

# first comparison
# second_transac = copy.deepcopy(following[0])

second_transac = following[0].copy()
record = compareTransac(record.copy(), second_transac)
for trade in following:
  next_tran = trade.copy()
  record = compareTransac(record.copy(), next_tran)
print(record)

