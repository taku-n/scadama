import MetaTrader5 as mt5

from enums import *

def send_order(order, symbol, price, lot, slip, stop, take):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        return 'Error: Getting symbol infomation failed.'

    if not symbol_info.select:
        return 'Error: Symbol is not selected.'

    pt = symbol_info.point

    if order == 'buy':
        type = mt5.ORDER_TYPE_BUY

        if stop != 0:
            sl = price - stop * pt
        else:
            sl = 0.0

        if take != 0:
            tp = price + take * pt
        else:
            tp = 0.0
    elif order == 'sell':
        type = mt5.ORDER_TYPE_SELL

        if stop != 0:
            sl = price + stop * pt
        else:
            sl = 0.0

        if take != 0:
            tp = price - take * pt
        else:
            tp = 0.0
    else:
        return 'Error: Invalid order type.'

    req = {
            'action': mt5.TRADE_ACTION_DEAL,
            'symbol': symbol,
            'volume': lot,
            'type': type,
            'price': price,
            'sl': sl,
            'tp': tp,
            'deviation': slip,
            'magic': 0,
            'comment': '',
            'type_time': mt5.ORDER_TIME_GTC,
            'type_filling': mt5.ORDER_FILLING_FOK,
    }

    return mt5.order_send(req)

def close(symbol):
    ps = mt5.positions_get(symbol=symbol)

    if len(ps) == 0:
        return 'No position.'

    for p in ps:
        result = close_position(p)

    return result

def close_ask(symbol):
    ps = mt5.positions_get(symbol=symbol)

    if len(ps) == 0:
        return 'No position.'

    for p in ps:
        if ENUM_ORDER_TYPE(p.type) == ENUM_ORDER_TYPE.ORDER_TYPE_BUY:
            result = close_position(p)

    return result

def close_bid(symbol):
    ps = mt5.positions_get(symbol=symbol)

    if len(ps) == 0:
        return 'No position.'

    for p in ps:
        if ENUM_ORDER_TYPE(p.type) == ENUM_ORDER_TYPE.ORDER_TYPE_SELL:
            result = close_position(p)

    return result

def close_all():
    ps = mt5.positions_get()

    if len(ps) == 0:
        return 'No position.'

    for p in ps:
        result = close_position(p)

    return result

def close_position(p):  # p is a TradePosition.
    req = {
            'action': mt5.TRADE_ACTION_DEAL,
            'price': p.price_current,
            'symbol': p.symbol,
            'volume': p.volume,
            'position': p.ticket,
    }

    if ENUM_ORDER_TYPE(p.type) == ENUM_ORDER_TYPE.ORDER_TYPE_BUY:
        req['type'] = mt5.ORDER_TYPE_SELL
    else:
        req['type'] = mt5.ORDER_TYPE_BUY

    return mt5.order_send(req)

def close_with_closing_by():
    pass

def close_ask_with_closing_by():
    pass

def close_bid_with_closing_by():
    pass

def close_all_with_closing_by():
    pass

def close_by(symbol):
    print('close_by()')
    close_by_recursively(symbol)

def close_by_recursively(symbol):
    print('close_by_recursively()')
    total = mt5.positions_total()
    print('total:', total)
    ps = mt5.positions_get(symbol=symbol)
    print('positions:', ps)
    print('len:', len(ps))

    if len(ps) < 2:
        print('returning')
        return

    pos = {}
    pos_by = {}

    for p in ps:
        if pos == {}:
            pos['type'] = ENUM_ORDER_TYPE(p.type)
            pos['ticket'] = p.ticket
        elif pos['type'] == ENUM_ORDER_TYPE.ORDER_TYPE_BUY:
            if ENUM_ORDER_TYPE(p.type) == ENUM_ORDER_TYPE.ORDER_TYPE_SELL:
                pos_by['type'] = ENUM_ORDER_TYPE(p.type)
                pos_by['ticket'] = p.ticket
                break
            else:
                continue
        elif pos['type'] == ENUM_ORDER_TYPE.ORDER_TYPE_SELL:
            if ENUM_ORDER_TYPE(p.type) == ENUM_ORDER_TYPE.ORDER_TYPE_BUY:
                pos_by['type'] = ENUM_ORDER_TYPE(p.type)
                pos_by['ticket'] = p.ticket
                break
            else:
                continue

    print('pos:', pos)
    print('pos_by:', pos_by)
    req = {
            'action': mt5.TRADE_ACTION_CLOSE_BY,
            'position': pos['ticket'],
            'position_by': pos_by['ticket'],
    }
    print('checking...')
    res = mt5.order_check(req)
    print('Check:', res)
    res = mt5.order_send(req)
    print('Response:', res)

    close_by_recursively(symbol)
