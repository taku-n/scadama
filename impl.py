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
from enums import *

class FrameMainImpl(ui.FrameMain):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self.q_ctrl      = None  # Queue:       Interprocess communication for control.
        self.q_tick      = None  # Queue:       Interprocess communication for ticks.
        self.symbols     = None  # list of str: All available symbol names.
        self.symbol      = None  # str:         A symbol that you are trading.
        self.symbol_info = None  # SymbolInfo:  Information of a symbol that you are trading.
        self.bid         = None  # float
        self.ask         = None  # float
        self.spread      = None  # int

        # MetaTrader5
        print('MetaTrader5 package version:', mt5.__version__)
        print('MetaTrader5 package author:', mt5.__author__)
        self.SetStatusText('MetaTrader5 package version: ' + mt5.__version__)

        # Load configuration.
        config = toml.load('config.toml')

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
        lot = self.spinctrldouble_lot.GetValue()
        slip = self.spinctrl_slippage.GetValue()
        sl = self.spinctrl_sl.GetValue()
        tp = self.spinctrl_tp.GetValue()

        code, msg = send_order('sell', self.symbol, event.price, lot, slip, sl, tp)

        if code == 'done':
            print('Done:', msg)
        else:
            print('Error:', msg)

    def on_ask_order(self, event):
        lot = self.spinctrldouble_lot.GetValue()
        slip = self.spinctrl_slippage.GetValue()
        sl = self.spinctrl_sl.GetValue()
        tp = self.spinctrl_tp.GetValue()

        code, msg = send_order('buy', self.symbol, event.price, lot, slip, sl, tp)

        if code == 'done':
            print('Done:', msg)
        else:
            print('Error:', msg)

    def on_setting_spin(self, event):
        symbol = self.symbol
        sp_lim = self.spinctrl_spread.GetValue()
        lot = self.spinctrldouble_lot.GetValue()
        slip = self.spinctrl_slippage.GetValue()
        sl = self.spinctrl_sl.GetValue()
        tp = self.spinctrl_tp.GetValue()

        if not os.path.exists('spin.toml'):
            init_spin_toml()
        spin_toml = toml.load('spin.toml')
        spin_toml['spin'][symbol] = {'sp_lim': sp_lim, 'lot': lot, 'slip': slip, 'sl': sl, 'tp': tp}
        with open('spin.toml', 'w') as f:
            toml.dump(spin_toml, f)

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
        print('symbol_info:', it.symbol_info)
        if not it.symbol_info.select:
            mt5.symbol_select(it.symbol, True)
        it.spinctrldouble_lot.SetMax(it.symbol_info.volume_max)
        set_spin(it, it.symbol)
        set_slippage_availability(it)

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

def set_slippage_availability(it):
    if ENUM_SYMBOL_TRADE_EXECUTION(it.symbol_info.trade_exemode) \
            == ENUM_SYMBOL_TRADE_EXECUTION.SYMBOL_TRADE_EXECUTION_REQUEST \
            or ENUM_SYMBOL_TRADE_EXECUTION(it.symbol_info.trade_exemode) \
            == ENUM_SYMBOL_TRADE_EXECUTION.SYMBOL_TRADE_EXECUTION_INSTANT:
        it.spinctrl_slippage.Enable()
    else:
        it.spinctrl_slippage.Disable()

def change_symbol(it, symbol):
    it.symbol = symbol
    symbol_info = it.symbol_info = mt5.symbol_info(symbol)

    if not symbol_info.select:
        mt5.symbol_select(symbol, True)
    it.spinctrldouble_lot.SetMax(symbol_info.volume_max)
    set_spin(it, symbol)

    it.q_ctrl.put(it.symbol)

def init_spin_toml():
    with open('spin.toml', mode='w') as f:
        f.write('''\
[spin.EURUSD]
sp_lim = 0
lot = 0.01
slip = 0
sl = 0
tp = 0
''')

def set_spin(it, symbol):
    if not os.path.exists('spin.toml'):
        init_spin_toml()
    spin_toml = toml.load('spin.toml')
    if symbol in spin_toml['spin']:
        spin_data = spin_toml['spin'][symbol]
        it.spinctrl_spread.SetValue(spin_data['sp_lim'])
        it.spinctrldouble_lot.SetValue(spin_data['lot'])
        it.spinctrl_slippage.SetValue(spin_data['slip'])
        it.spinctrl_sl.SetValue(spin_data['sl'])
        it.spinctrl_tp.SetValue(spin_data['tp'])
    else:
        it.spinctrl_spread.SetValue(0)
        it.spinctrldouble_lot.SetValue(0.0)
        it.spinctrl_slippage.SetValue(0)
        it.spinctrl_sl.SetValue(0)
        it.spinctrl_tp.SetValue(0)

def send_order(order, symbol, price, lot, slip, stop, take):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        return 'error', 'Getting symbol infomation failed.'

    if not symbol_info.select:
        return 'error', 'Symbol is not selected.'

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
        return 'error', 'Invalid order type.'

    req = {'action': mt5.TRADE_ACTION_DEAL,
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
            'type_filling': mt5.ORDER_FILLING_FOK}

    print(req)
    res = mt5.order_send(req)

    print(res)

    if res.retcode == mt5.TRADE_RETCODE_DONE:
        return 'done', res
    else:
        return 'error', res
