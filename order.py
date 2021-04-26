import MetaTrader5 as mt5

def close(symbol):
    ps = mt5.positions_get(symbol=symbol)
