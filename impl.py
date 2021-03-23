import datetime
import locale
from multiprocessing import *
import os
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

        # Setup queues.
        self.q_ctrl = Queue()  # Interprocess Communication for controlling a process.
        self.q_tick = Queue()  # Interprocess Communication for ticks.

        # Main Window Size
        size = config['size']
        if size['x'] != 0:
            self.SetSize(wx.Size(size['x'], size['y']))

        # choice_client
        client = config['client']
        self.choice_client.Set(client)
        self.choice_client.SetSelection(0)

        # Initialize a symbol.
        quick_symbols = config['symbol']
        self.symbol = quick_symbols[0]
        self.symbols = []

    def on_connection(self, event):
        if self.togglebutton_connect.GetValue():  # Pressed
            connect(self)
        else:  # Pulled
            disconnect(self)

    def on_symbol_selection(self, event):
        symbol = self.combobox_symbol.GetStringSelection()
        change_symbol(self, symbol)

    def on_symbol_input(self, event):
        symbol = self.combobox_symbol.GetValue()
        if symbol in self.symbols:
            change_symbol(self, symbol)
            self.combobox_symbol.SetStringSelection(self.symbol)

    def on_bid_order(self, event):
        print('Bid:', event.price)
        print(round(self.spinctrldouble_spread.GetValue(), 1))

    def on_ask_order(self, event):
        print('Ask:', event.price)
        print(round(self.spinctrldouble_spread.GetValue(), 1))

    def on_close(self, event):
        self.q_ctrl.put('disconnect')  # Child Process Disconnection
        mt5.shutdown()
        self.Destroy()

def connect(it):
    client = it.choice_client.GetStringSelection()

    if mt5.initialize(client):  # Success
        it.choice_client.Disable()
        it.togglebutton_connect.SetLabel('Disconnect')
        print('Connected to', client)
        it.SetStatusText('Connected to ' + client)
        print('Terminal Info:', mt5.terminal_info())
        print('MetaTrader 5 version:', mt5.version())

        # combobox_symbol

        symbols_info = mt5.symbols_get()
        symbols = []
        for x in symbols_info:
            symbols.append(x.name)
        it.symbols = symbols

        it.combobox_symbol.Set(it.symbols)

        if it.symbol in it.symbols:
            it.combobox_symbol.SetStringSelection(it.symbol)
        else:
            it.combobox_symbol.SetSelection(0)
            it.symbol = it.combobox_symbol.GetStringSelection()

        it.symbol_info = mt5.symbol_info(it.symbol)
        if not it.symbol_info.select:
            mt5.symbol_select(it.symbol, True)
        it.spinctrldouble_lot.SetMax(it.symbol_info.volume_max)

        # A thread to receive a tick.
        thread = Thread(target = recv_tick, args = (it, ))
        thread.start()

        # A process to send a tick.
        process = Process(target = send_tick, args = (it.q_ctrl, it.q_tick))
        process.start()
        it.q_ctrl.put(it.choice_client.GetStringSelection())
        it.q_ctrl.put(it.symbol)

    else:  # Failure
        it.togglebutton_connect.SetValue(False)
        print('Failed to connect to', client)
        print(last_error())

def disconnect(it):
    client = it.choice_client.GetStringSelection()

    it.q_ctrl.put('disconnect')  # Child Process Disconnection
    mt5.shutdown()
    print('Disconnected from', client)
    it.SetStatusText('Disconnected from ' + client)
    it.choice_client.Enable()
    it.combobox_symbol.Clear()
    it.togglebutton_connect.SetLabel('Connect')

def recv_tick(it):  # Runs in a thread.
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

    while True:
        # Get a tick.
        tick = it.q_tick.get()  # e.g. {'time': 1616153185, 'bid': 1.19124, 'ask': 1.19127,
                                # 'last': 0.0, 'volume': 0, 'time_msc': 1616153185151, 'flags': 4,
                                # 'volume_real': 0.0, 'symbol': 'EURUSD', 'error': ''}

        # Show the server's local time.

        time = tick['time']

        # This does not mean it is UTC but server's local time.
        time_zone = datetime.timezone(datetime.timedelta(hours = 0))
        time = datetime.datetime.fromtimestamp(time, time_zone)
        time_str = f'{time:%Y.%m.%d %a %H:%M:%S}'  # f-string

        it.statictext_time.SetLabel(time_str)

        # Show bid, ask and spread.

        it.bid = tick['bid']
        it.orderbutton_bid.update_price(it.bid, it.symbol_info.digits)

        it.ask = tick['ask']
        it.orderbutton_ask.update_price(it.ask, it.symbol_info.digits)

        it.spread = round((it.ask - it.bid) * (10.0 ** it.symbol_info.digits))
        it.statictext_spread.SetLabel(f'{it.spread}')

        if tick['error'] != '':
            it.SetStatusText(f'Error: {tick["error"]}')
        continue

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

            tick = mt5.symbol_info_tick(symbol)  # Non-blocking

            if tick != None:
                if tick != last_tick:
                    last_tick = tick
                    tick_d = tick._asdict()
                    tick_d['symbol'] = symbol
                    tick_d['error'] = ''
                    q_tick.put(tick_d)
            else:
                # Double parens by structseq()
                #                time  bid  ask  last  volume  time_msc  flags  volume_real
                tick = mt5.Tick((   0, 0.0, 0.0,  0.0,      0,        0,     0,         0.0))

                if tick != last_tick:
                    last_tick = tick
                    tick_d = tick._asdict()
                    tick_d['symbol'] = symbol
                    tick_d['error'] = 'Getting a symbol info tick failed.'
                    q_tick.put(tick_d)

            sleep(0.001)

def change_symbol(it, symbol):
    it.symbol = symbol
    it.symbol_info = mt5.symbol_info(it.symbol)
    if not it.symbol_info.select:
        mt5.symbol_select(it.symbol, True)
    it.spinctrldouble_lot.SetValue(0.0)
    it.spinctrldouble_lot.SetMax(it.symbol_info.volume_max)
    it.q_ctrl.put(it.symbol)

def send_order(it):
    print(round(it.spinctrldouble_spread.GetValue(), 1))
