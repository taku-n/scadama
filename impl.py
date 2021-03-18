from multiprocessing import *
from queue import Queue
from threading import *

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
    else:  # Failure
        instance.togglebutton_connect.SetValue(False)
        print('Failed to connect to', client)

def disconnect(instance):
    client = instance.choice_client.GetStringSelection()

    mt5.shutdown()
    print('Disconnected from', client)
    instance.SetStatusText('Disconnected from ' + client)
    instance.choice_client.Enable()
    instance.combobox_symbol.Clear()
    instance.togglebutton_connect.SetLabel('Connect')
