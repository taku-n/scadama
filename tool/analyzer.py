# analyzer.py 1970 1

import calendar
from datetime import datetime
import sys

import MetaTrader5 as mt5

def main():
    args = sys.argv

    print('MetaTrader5 Package Version:', mt5.__version__)

    if not mt5.initialize():
        print('initialize() failed. Error code:', mt5.last_error())
        quit()
    account_info = mt5.account_info()._asdict()
    print('company:', account_info['company'])
    print('server:', account_info['server'])
    print('login:', account_info['login'])
    print('balance:', account_info['balance'])
    print()

    print_monthly(int(args[1]), int(args[2]))

# 月またぎの処理は未対応
def print_monthly(year, month):
    from_date = datetime(year, month, 1)
    to_date = datetime(year, month, calendar.monthrange(year, month)[1])

    print(year, str(month).zfill(2))
    deals_total = mt5.history_deals_total(from_date, to_date)
    print('Total Deals:', deals_total)
    if deals_total == 0:
        return

    deals = mt5.history_deals_get(from_date, to_date)
    total_profit = 0.0
    total_win = 0.0
    total_loss = 0.0
    total_lose = 0.0
    for x in deals:
        if x.entry == 1:  # Ignoring closing order.
            continue
        position_id = x.position_id
        symbol = x.symbol
        if x.type == 0:
            position_type = 'BUY'
        else:
            position_type = 'SELL'
        volume = x.volume
        open_price = x.price
        commission = x.commission
        for y in deals:
            if y.entry == 0:  # Ignoring opening order.
                continue
            if y.position_id == position_id:
                close_price = y.price
                if x.type == 0:  # Buying.
                    difference = close_price - open_price
                else:  # Selling.
                    difference = open_price - close_price
                swap = y.swap
                profit = y.profit
                if profit >= 0:
                    total_profit += profit
                    total_win += 1.0
                else:
                    total_loss += abs(profit)
                    total_lose += 1.0
        print(f'{position_id} {symbol} {position_type:4} {volume} {open_price:10.5f} {close_price:10.5f} {difference:8.5f} {commission:7} {swap:4} {profit:9}')
    print(f'Profit: {total_profit}, Loss: {total_loss}, Total: {total_profit - total_loss}')
    print(f'Win: {total_win}, Lose: {total_lose}, Winning Rate: {total_win / (total_win + total_lose):.3f}')
    rrr = total_profit / total_loss
    print(f'Risk Reward Ratio: {rrr:.3f}, Needed Winning Rate: {1.0 / (rrr + 1.0):.3f}')


if __name__ == '__main__':
    main()
