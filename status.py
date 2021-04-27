import datetime

import MetaTrader5 as mt5

def estimate_commission(symbol):  # Estimate commission from history.
    from_date = datetime.datetime.now() - datetime.timedelta(days=180)
    to_date   = datetime.datetime.now()

    ds = mt5.history_deals_get(from_date, to_date, group=symbol)

    sum = 0.0
    n = 0
    for d in ds:
        if d.entry == 0:  # 0 is opening a position. 1 is closing. Cost you it when opening.
            sum += -d.commission * (1.0 / d.volume)
            n += 1

    if n != 0:
        estimated_commission = sum / n
    else:
        estimated_commission = None

    return estimated_commission
