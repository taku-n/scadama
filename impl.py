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
import impl_config
import order
import status
from enums import *

class FrameMainImpl(ui.FrameMain):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self.VERSION          = '1.1.2'

        self.q_ctrl           = None  # Queue:       Interprocess communication for control.
        self.q_tick           = None  # Queue:       Interprocess communication for ticks.
        self.account_currency = None  # str
        self.account_currency_digits = None  # int
        self.account_number   = None  # int
        self.symbols          = None  # list of str: All available symbol names.
        self.symbol           = None  # str:         A symbol that you are trading.
        self.symbol_info      = None  # SymbolInfo:  Information of a symbol that you are trading.
        self.can_close_by     = None  # bool:        True: Can close a position by another one.
        self.bid              = None  # float
        self.ask              = None  # float
        self.spread           = None  # int

        # MetaTrader5
        self.SetStatusText(f'Scadama {self.VERSION}, MetaTrader5 package {mt5.__version__}')

        # Load configuration.
        if not os.path.exists('config.toml'):
            init_config_toml()
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

    def on_config(self, event):
        impl_config.FrameConfigImpl(wx.GetTopLevelParent(self), wx.ID_ANY)

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

        result = order.send_order('sell', self.symbol, event.price, lot, slip, sl, tp)

        if type(result) is mt5.OrderSendResult:
            self.SetStatusText(f'{result.retcode}: {result.comment}')
        else:
            self.SetStatusText(result)

    def on_ask_order(self, event):
        lot = self.spinctrldouble_lot.GetValue()
        slip = self.spinctrl_slippage.GetValue()
        sl = self.spinctrl_sl.GetValue()
        tp = self.spinctrl_tp.GetValue()

        result = order.send_order('buy', self.symbol, event.price, lot, slip, sl, tp)

        if type(result) is mt5.OrderSendResult:
            self.SetStatusText(f'{result.retcode}: {result.comment}')
        else:
            self.SetStatusText(result)


    def on_setting_spin(self, event):
        symbol = self.symbol
        sp_lim = self.spinctrl_spread.GetValue()
        lot = self.spinctrldouble_lot.GetValue()
        slip = self.spinctrl_slippage.GetValue()
        sl = self.spinctrl_sl.GetValue()
        tp = self.spinctrl_tp.GetValue()

        if os.path.exists('spin.toml'):
            spin_toml = toml.load('spin.toml')
        else:
            spin_toml = {}

        spin_toml[symbol] = {'sp_lim': sp_lim, 'lot': lot, 'slip': slip, 'sl': sl, 'tp': tp}
        with open('spin.toml', 'w') as f:
            toml.dump(spin_toml, f)

        # Don't forget to check "Store as attribute" on wxGlade to change StaticText value.
        estimated_commission_per_lot = status.estimate_commission(self.symbol)
        if estimated_commission_per_lot:
            digit = self.account_currency_digits + 3
            self.statictext_commission_per_lot_value.SetLabel(
                    f'{estimated_commission_per_lot:.{digit}f}')
            estimated_commission = estimated_commission_per_lot * lot
            self.statictext_commission_value.SetLabel(f'{estimated_commission:.{digit}f}')
        else:
            self.statictext_commission_value.SetLabel('No data.')

    def on_closing_bid(self, event):
        if self.can_close_by:
            order.close_bid_with_closing_by()
            self.SetStatusText('Not implemented.')
        else:
            result = order.close_bid(self.symbol)
            if type(result) is mt5.OrderSendResult:
                self.SetStatusText(f'{result.retcode}: {result.comment}')
            else:
                self.SetStatusText(result)

    def on_closing_all(self, event):
        if self.can_close_by:
            order.close_all_with_closing_by()
            self.SetStatusText('Not implemented.')
        else:
            result = order.close_all()
            if type(result) is mt5.OrderSendResult:
                self.SetStatusText(f'{result.retcode}: {result.comment}')
            else:
                self.SetStatusText(result)

    def on_closing(self, event):
        if self.can_close_by:
            order.close_with_closing_by()
            self.SetStatusText('Not implemented.')
        else:
            result = order.close(self.symbol)
            if type(result) is mt5.OrderSendResult:
                self.SetStatusText(f'{result.retcode}: {result.comment}')
            else:
                self.SetStatusText(result)

    def on_closing_ask(self, event):
        if self.can_close_by:
            order.close_ask_with_closing_by()
            self.SetStatusText('Not implemented.')
        else:
            result = order.close_ask(self.symbol)
            if type(result) is mt5.OrderSendResult:
                self.SetStatusText(f'{result.retcode}: {result.comment}')
            else:
                self.SetStatusText(result)

    def on_closing_by(self, event):
        order.close_by(self.symbol)

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
        print('MetaTrader 5 version:', mt5.version())

        terminal_info = mt5.terminal_info()
        if not terminal_info.trade_allowed:
            it.SetStatusText('Trading is not allowed. (Tools -> Options -> Expert Advisors).')

        account_info = mt5.account_info()

        if ENUM_ACCOUNT_TRADE_MODE(account_info.trade_mode) \
                == ENUM_ACCOUNT_TRADE_MODE.ACCOUNT_TRADE_MODE_DEMO:
            it.SetTitle('Scadama [DEMO]')
        elif ENUM_ACCOUNT_TRADE_MODE(account_info.trade_mode) \
                == ENUM_ACCOUNT_TRADE_MODE.ACCOUNT_TRADE_MODE_CONTEST:
            it.SetTitle('Scadama [CONTEST]')
        else:
            it.SetTitle('Scadama')

        it.account_number          = account_info.login
        it.account_currency        = account_info.currency
        it.account_currency_digits = account_info.currency_digits

        # combobox_symbol and initializing symbol

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
        set_spin(it, it.symbol)
        set_slippage_availability(it)
        set_close_by_availability(it)

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

def init_config_toml():
    with open('config.toml', mode='w') as f:
        f.write('''\
# Paths to your MetaTrader 5 clients.
client = [
  'C:\local\mt5\mq\\terminal64.exe',
  'C:\local\mt5\\tt\\terminal64.exe',
  'C:\your\mt5\\terminal64.exe',
]

# Symbols for quick buttons.
symbol = [
  'EURUSD',
  'USDJPY',
]

# Main Window Size
# If the x value is 0, the window size will be decided automatically.
# [Windows] If you get the window scale setting 200%,
#           the window size will be twice as large as this settings.
[size]
x = 0
y = 0
''')

def set_slippage_availability(it):
    if ENUM_SYMBOL_TRADE_EXECUTION(it.symbol_info.trade_exemode) \
            == ENUM_SYMBOL_TRADE_EXECUTION.SYMBOL_TRADE_EXECUTION_REQUEST \
            or ENUM_SYMBOL_TRADE_EXECUTION(it.symbol_info.trade_exemode) \
            == ENUM_SYMBOL_TRADE_EXECUTION.SYMBOL_TRADE_EXECUTION_INSTANT:
        it.spinctrl_slippage.Enable()
    else:
        it.spinctrl_slippage.Disable()

def set_close_by_availability(it):
    if SYMBOL_ORDER_MODE(it.symbol_info.order_mode) & SYMBOL_ORDER_MODE.SYMBOL_ORDER_CLOSEBY \
            != SYMBOL_ORDER_MODE(0):
        it.can_close_by = True
        it.button_close_by.Enable()
    else:
        it.can_close_by = False
        it.button_close_by.Disable()

def change_symbol(it, symbol):
    it.symbol = symbol
    symbol_info = it.symbol_info = mt5.symbol_info(symbol)

    if not symbol_info.select:
        mt5.symbol_select(symbol, True)
    it.spinctrldouble_lot.SetMax(symbol_info.volume_max)
    set_spin(it, symbol)
    set_slippage_availability(it)
    set_close_by_availability(it)

    it.q_ctrl.put(it.symbol)

def set_spin(it, symbol):
    if os.path.exists('spin.toml'):
        spin_toml = toml.load('spin.toml')
    else:
        spin_toml = {}

    lot = 0.0
    if symbol in spin_toml:
        spin_data = spin_toml[symbol]
        it.spinctrl_spread.SetValue(spin_data['sp_lim'])
        it.spinctrldouble_lot.SetValue(spin_data['lot'])
        it.spinctrl_slippage.SetValue(spin_data['slip'])
        it.spinctrl_sl.SetValue(spin_data['sl'])
        it.spinctrl_tp.SetValue(spin_data['tp'])
        lot = spin_data['lot']
    else:
        it.spinctrl_spread.SetValue(0)
        it.spinctrldouble_lot.SetValue(0.0)
        it.spinctrl_slippage.SetValue(0)
        it.spinctrl_sl.SetValue(0)
        it.spinctrl_tp.SetValue(0)

    estimated_commission_per_lot = status.estimate_commission(it.symbol)
    if estimated_commission_per_lot:
        digit = it.account_currency_digits + 3
        it.statictext_commission_per_lot_value.SetLabel(
                f'{estimated_commission_per_lot:.{digit}f}')
        estimated_commission = estimated_commission_per_lot * lot
        it.statictext_commission_value.SetLabel(f'{estimated_commission:.{digit}f}')
    else:
        it.statictext_commission_value.SetLabel('No data.')
