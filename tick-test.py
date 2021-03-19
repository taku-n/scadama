import MetaTrader5 as mt5

def main():
    client = 'C:\local\mt5\mq\\terminal64.exe'
    symbol = 'EURUSD'
    last_tick = None

    mt5.initialize(client)

    for i in range(10):
        tick = mt5.symbol_info_tick(symbol)._asdict()
        print('tick (immediately):    ', tick)

        if tick != last_tick:
            print('tick (comparison):     ', tick)
            print('last_tick (comparison):', last_tick)
            print(id(tick))
            print(id(last_tick))
            last_tick = tick
            print('last_tick (after_comparison):', last_tick)
            print(id(tick))
            print(id(last_tick))
            tick['symbol'] = symbol

        print('--------')

    mt5.shutdown()

if __name__ == '__main__':
    main()
