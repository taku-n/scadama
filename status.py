import datetime
import math

import MetaTrader5 as mt5

from enums import *

def update_average(it):
    ps = mt5.positions_get(symbol=it.symbol)
    buy_sum = 0.0
    buy_lot = 0.0
    sell_sum = 0.0
    sell_lot = 0.0

    for p in ps:
        if p.type == 0:  # Buy position.
            buy_sum += p.price_open * p.volume
            buy_lot += p.volume
        elif p.type == 1:  # Sell position.
            sell_sum += p.price_open * p.volume
            sell_lot += p.volume

    if buy_lot != 0.0:
        it.statictext_average_buy.SetLabel(f'{(buy_sum / buy_lot):.{it.symbol_info.digits}f}')
    else:
        it.statictext_average_buy.SetLabel('0')

    if sell_lot != 0.0:
        it.statictext_average_sell.SetLabel(f'{(sell_sum / sell_lot):.{it.symbol_info.digits}f}')
    else:
        it.statictext_average_sell.SetLabel('0')

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
        it.statictext_commission_per_lot_value.SetLabel('No data.')

def estimate_commission(symbol):  # Estimate commission from history.
    from_date = datetime.datetime.now() - datetime.timedelta(days=180)

    # Workaround: mt5.history_deals_get() does not get today's data.
    to_date   = datetime.datetime.now() + datetime.timedelta(days=1)

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
    swap_long_per_lot, swap_short_per_lot = calculate_swap(it)
    lot = it.spinctrldouble_lot.GetValue()
    day_of_week = get_day_of_week_str(ENUM_DAY_OF_WEEK(it.symbol_info.swap_rollover3days))

    if not math.isnan(swap_long_per_lot):
        swap_long = swap_long_per_lot * lot
        swap_short = swap_short_per_lot * lot
        digit = it.account_currency_digits

        it.statictext_swap_long_value.SetLabel(f'{swap_long:.{digit}f}')
        it.statictext_swap_long_per_lot_value.SetLabel(f'{swap_long_per_lot:.{digit}f}')
        it.statictext_swap_short_value.SetLabel(f'{swap_short:.{digit}f}')
        it.statictext_swap_short_per_lot_value.SetLabel(f'{swap_short_per_lot:.{digit}f}')
        it.statictext_swap_x3_value.SetLabel(day_of_week)
    else:
        it.statictext_swap_long_value.SetLabel('N/A')
        it.statictext_swap_long_per_lot_value.SetLabel('N/A')
        it.statictext_swap_short_value.SetLabel('N/A')
        it.statictext_swap_short_per_lot_value.SetLabel('N/A')
        it.statictext_swap_x3_value.SetLabel(day_of_week)

def calculate_swap(it):
    if it.account_currency == 'USD':
        return math.nan, math.nan
    elif it.account_currency == 'EUR':
        return math.nan, math.nan
    elif it.account_currency == 'JPY':
        if ENUM_SYMBOL_SWAP_MODE(it.symbol_info.swap_mode) \
                == ENUM_SYMBOL_SWAP_MODE.SYMBOL_SWAP_MODE_POINTS:
            if it.symbol_info.currency_profit == 'JPY':
                swap_long = it.symbol_info.point * it.symbol_info.swap_long \
                        * it.symbol_info.trade_contract_size
                swap_short = it.symbol_info.point * it.symbol_info.swap_short \
                        * it.symbol_info.trade_contract_size

                return swap_long, swap_short
            elif it.symbol_info.currency_profit == 'USD':
                swap_long_in_usd = it.symbol_info.point * it.symbol_info.swap_long \
                        * it.symbol_info.trade_contract_size
                swap_short_in_usd = it.symbol_info.point * it.symbol_info.swap_short \
                        * it.symbol_info.trade_contract_size

                usdjpy = mt5.symbol_info_tick('USDJPY')
                usdjpy_middle_rate = (usdjpy.ask + usdjpy.bid) / 2  # For a flash huge spread.
                swap_long = swap_long_in_usd * usdjpy_middle_rate
                swap_short = swap_short_in_usd * usdjpy_middle_rate

                return swap_long, swap_short
            else: 
                return math.nan, math.nan
        else:
            return math.nan, math.nan
    else:
        return math.nan, math.nan

def get_day_of_week_str(enum_day_of_week):
    if enum_day_of_week == ENUM_DAY_OF_WEEK.SUNDAY:
        return 'Sunday'
    elif enum_day_of_week == ENUM_DAY_OF_WEEK.MONDAY:
        return 'Monday'
    elif enum_day_of_week == ENUM_DAY_OF_WEEK.TUESDAY:
        return 'Tuesday'
    elif enum_day_of_week == ENUM_DAY_OF_WEEK.WEDNESDAY:
        return 'Wednesday'
    elif enum_day_of_week == ENUM_DAY_OF_WEEK.THURSDAY:
        return 'Thursday'
    elif enum_day_of_week == ENUM_DAY_OF_WEEK.FRIDAY:
        return 'Friday'
    elif enum_day_of_week == ENUM_DAY_OF_WEEK.SATURDAY:
        return 'Saturday'
    else:
        return 'Invalid'

def update_margin(it):
    lot = it.spinctrldouble_lot.GetValue()
    price = it.symbol_info.ask

    if lot != 0.0:
        margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, it.symbol, lot, price)
        margin_per_lot = margin / lot
    else:
        margin = 0
        margin_per_lot = 0

    it.statictext_margin_value.SetLabel(f'{margin:.{it.account_currency_digits}f}')
    it.statictext_margin_per_lot_value.SetLabel(f'{margin_per_lot:.{it.account_currency_digits}f}')
