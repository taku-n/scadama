# $ python -m inspect

import sys

import MetaTrader5 as mt5

def main():
    print('''Type "initialize('PATH-TO-YOUR-CLIENT')" to connect.''')
    print('    When you use "\\t" in your path, use "\\\\t" instead.')
    print("    e.g. initialize('C:\path\\\\to\your\\\\terminal64.exe').")
    print('Type "help" to get how to use.')
    print('Type "exit" to exit this program.')

    while True:
        print('> ', end='')
        cmd = input()
        if cmd == 'help':
            help()
        elif cmd == 'exit':
            shutdown()
            sys.exit()
        elif cmd == 'disconnect':
            shutdown()
        elif cmd == 'version':
            version()
        elif cmd == 'terminal_info':
            terminal_info()
        elif cmd == 'account_info':
            account_info()
        elif cmd == 'symbols_total':
            symbols_total()
        elif cmd == 'symbols_get':
            symbols_get(None)
        elif cmd == '':
            continue
        else:
            eval(cmd)

def help():
    print('''\
initialize('PATH-TO-YOUR-CLIENT')
    When you use "\\t" in your path, use "\\\\t" instead.
    e.g. initialize('C:\path\\\\to\your\\\\terminal64.exe').
disconnect
exit

help
version
terminal_info
account_info
symbols_total
symbols_get
    symbols_get('FILTER')
    e.g. symbols_get('EURUSD')
         symbols_get('*USD')
         symbols_get('*,!*USD')
symbol_info('SYMBOL')
    e.g. symbol_info('EURUSD')
''', end='')

def initialize(client):
    b = mt5.initialize(client)
    if b:
        print('Connected.')
    else:
        print(f'Failed to connect. Error: {mt5.last_error()}.')

def shutdown():
    mt5.shutdown()
    print('Disconnected.')

def version():
    terminal_version, build, release_date = mt5.version()
    print('MetaTrader 5 Terminal')
    print('         Version:', terminal_version)
    print('           Build:', build)
    print('    Release Date:', release_date)

def terminal_info():
    d = mt5.terminal_info()._asdict()
    for k in d:
        print(f'{k:>21}: {d[k]}')

def account_info():
    info = mt5.account_info()
    if info == None:
        print('Not connected yet.')
        return

    d = info._asdict()
    for k in d:
        print(f'{k:>18}: {d[k]}')

def symbols_total():
    n = mt5.symbols_total()
    print(f'The number of symbols is {n}.')

def symbols_get(filter):
    if filter == None:
        ss = mt5.symbols_get()
    else:
        ss = mt5.symbols_get(filter)

    if ss == None:
        print('Not connected yet.')
        return

    for s in ss:
        print('name:', s.name)
        print(s)
        print('')

def symbol_info(symbol):
    s = mt5.symbol_info(symbol)

    if s == None:
        print('Not connected yet.')
        return

    d = s._asdict()
    for k in d:
        if k == 'point':
            print(f'{k:>26}: {d[k]:f}')
        elif k == 'trade_tick_size':
            print(f'{k:>26}: {d[k]:f}')
        else:
            print(f'{k:>26}: {d[k]}')

        if k == 'trade_mode':
            print('0: SYMBOL_TRADE_MODE_DISABLED,',
                    '1: SYMBOL_TRADE_MODE_LONGONLY,',
                    '2: SYMBOL_TRADE_MODE_SHORTONLY,',
                    '3: SYMBOL_TRADE_MODE_CLOSEONLY,',
                    '4: SYMBOL_TRADE_MODE_FULL')
        elif k == 'trade_exemode':
            print('0: SYMBOL_TRADE_EXECUTION_REQUEST,',    # order_send() deviation works.
                    '1: SYMBOL_TRADE_EXECUTION_INSTANT,',  # order_send() deviation works.
                    '2: SYMBOL_TRADE_EXECUTION_MARKET,',
                    '3: SYMBOL_TRADE_EXECUTION_EXCHANGE')

if __name__ == '__main__':
    main()
