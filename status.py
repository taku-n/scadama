import datetime

import MetaTrader5 as mt5

def update_commission(it):
    lot = it.spinctrldouble_lot.GetValue()

    # Don't forget to check "Store as attribute" on wxGlade to change StaticText value.
    estimated_commission_per_lot = estimate_commission(it.symbol)
    if estimated_commission_per_lot:
        digit = it.account_currency_digits + 3
        it.statictext_commission_per_lot_value.SetLabel(
            f'{estimated_commission_per_lot:.{digit}f}')
        estimated_commission = estimated_commission_per_lot * lot
        it.statictext_commission_value.SetLabel(f'{estimated_commission:.{digit}f}')
    else:
        it.statictext_commission_value.SetLabel('No data.')

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

def update_swap(it):
    pass
