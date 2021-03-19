from multiprocessing import *
from threading import *
from time import sleep

import MetaTrader5 as mt5
import toml
import wx.stc

import ui

class FrameMainImpl(ui.FrameMain):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        # MetaTrader5
        print('MetaTrader5 package version:', mt5.__version__)
        print('MetaTrader5 package author:', mt5.__author__)
        self.SetStatusText('MetaTrader5 package version: ' + mt5.__version__)

        # Load configuration.
        config = toml.load(open('config.toml'))

        # choice_client
        client = config['client']
        self.choice_client.Set(client)
        self.choice_client.SetSelection(0)

        symbols = config['symbol']
        self.symbol = symbols[0]

    def on_connection(self, event):
        if self.togglebutton_connect.GetValue():  # Pressed
            connect(self)
        else:  # Pulled
            disconnect(self)

def connect(instance):
    client = instance.choice_client.GetStringSelection()

    if mt5.initialize(client):  # Success
        instance.choice_client.Disable()
        instance.togglebutton_connect.SetLabel('Disconnect')
        print('Connected to', client)
        instance.SetStatusText('Connected to ' + client)
        print('Terminal Info:', mt5.terminal_info())
        print('MetaTrader 5 version:', mt5.version())

        # combobox_symbol

        symbol_info = mt5.symbols_get()
        symbol = []
        for x in symbol_info:
            symbol.append(x.name)
        instance.combobox_symbol.Set(symbol)

        if instance.symbol in symbol:
            instance.combobox_symbol.SetStringSelection(instance.symbol)
        else:
            instance.combobox_symbol.SetSelection(0)
            instance.symbol = instance.combobox_symbol.GetStringSelection()

        instance.symbol_info = mt5.symbol_info(instance.symbol)

        instance.q_ctrl = Queue()  # Interprocess Communication for controlling a process.
        q_tick = Queue()  # Interprocess Communication for ticks.

        # A thread to receive a tick.
        thread = Thread(target = recv_tick, args = (instance, q_tick))
        thread.start()

        # A process to send a tick.
        process = Process(target = send_tick, args = (instance.q_ctrl, q_tick))
        process.start()
        instance.q_ctrl.put(instance.choice_client.GetStringSelection())
        instance.q_ctrl.put(instance.symbol)

    else:  # Failure
        instance.togglebutton_connect.SetValue(False)
        print('Failed to connect to', client)

def disconnect(instance):
    client = instance.choice_client.GetStringSelection()

    instance.q_ctrl.put('disconnect')  # Child Process Disconnection
    mt5.shutdown()
    print('Disconnected from', client)
    instance.SetStatusText('Disconnected from ' + client)
    instance.choice_client.Enable()
    instance.combobox_symbol.Clear()
    instance.togglebutton_connect.SetLabel('Connect')

def recv_tick(instance, q_tick):  # Runs in a thread.
    while True:
        # Get a tick.
        tick = q_tick.get()  # e.g. {'time': 1616153185, 'bid': 1.19124, 'ask': 1.19127,
                             # 'last': 0.0, 'volume': 0, 'time_msc': 1616153185151, 'flags': 4,
                             # 'volume_real': 0.0, 'symbol': 'EURUSD'}
        print(tick)
        print(instance.symbol_info.currency_profit)
        continue

        # Show the servers local time.

        try:
            time = tick['time']
        except Exception as e:
            if e.args != ():
                pass
                #write_log(f'Error, getting a time: {e.args}')
            sys.exit()

        # This doesnt mean it is UTC but a servers local time.
        time_zone = datetime.timezone(datetime.timedelta(hours = 0))

        time = datetime.datetime.fromtimestamp(time, time_zone)
        time = f'{time:%Y.%m.%d %a %H:%M:%S}'  # f-string

        try:
            label_time.configure(text = time)
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        # Set a symbol.
        Tick.symbol = tick['symbol']

        # Show ask, bid and spread.

        try:
            ask = tick['ask']
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        Tick.ask = ask

        try:
            bid = tick['bid']
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        Tick.bid = bid

        spread = (ask - bid) * 10000.0
        Tick.spread = spread

        try:
            button_ask.configure(text = f'{ask:.5f}')
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        try:
            button_bid.configure(text = f'{bid:.5f}')
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        try:
            label_spread.configure(text = f'{spread:.1f}')
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

def send_tick(q_ctrl, q_tick):  # Runs in a child process.
    client = q_ctrl.get()

    if mt5.initialize(client):  # Success
        symbol = q_ctrl.get()
        last_tick = None

        while True:
            if not q_ctrl.empty():
                ctrl = q_ctrl.get()
                if ctrl == 'disconnect':
                    mt5.shutdown()
                    return
                else:
                    symbol = ctrl

            tick = mt5.symbol_info_tick(symbol)._asdict()  # Non-blocking

            if tick != last_tick:
                last_tick = tick.copy()
                tick['symbol'] = symbol
                q_tick.put(tick)

            sleep(0.001)
