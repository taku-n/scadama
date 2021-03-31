# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Wed Mar 24 03:35:43 2021
#

import wx


import widget


class FrameMain(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("Scadama")

        self.statusbar_main = self.CreateStatusBar(1)
        self.statusbar_main.SetStatusWidths([-1])

        self.panel_main = wx.Panel(self, wx.ID_ANY)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_client = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_client, 0, wx.EXPAND, 0)

        self.button_config = wx.Button(self.panel_main, wx.ID_ANY, u"⚙", style=wx.BU_EXACTFIT)
        sizer_client.Add(self.button_config, 0, 0, 0)

        self.choice_client = wx.Choice(self.panel_main, wx.ID_ANY, choices=[])
        sizer_client.Add(self.choice_client, 1, 0, 0)

        self.togglebutton_connect = wx.ToggleButton(self.panel_main, wx.ID_ANY, "Connect")
        sizer_client.Add(self.togglebutton_connect, 0, 0, 0)

        gridsizer_symbol_copy = wx.GridSizer(2, 3, 0, 0)
        sizer_main.Add(gridsizer_symbol_copy, 0, wx.EXPAND, 0)

        self.button_9 = wx.Button(self.panel_main, wx.ID_ANY, "button_9")
        gridsizer_symbol_copy.Add(self.button_9, 0, 0, 0)

        self.button_10 = wx.Button(self.panel_main, wx.ID_ANY, "button_10")
        gridsizer_symbol_copy.Add(self.button_10, 0, 0, 0)

        self.button_11 = wx.Button(self.panel_main, wx.ID_ANY, "button_11")
        gridsizer_symbol_copy.Add(self.button_11, 0, 0, 0)

        self.button_12 = wx.Button(self.panel_main, wx.ID_ANY, "button_12")
        gridsizer_symbol_copy.Add(self.button_12, 0, 0, 0)

        self.button_13 = wx.Button(self.panel_main, wx.ID_ANY, "button_13")
        gridsizer_symbol_copy.Add(self.button_13, 0, 0, 0)

        self.button_14 = wx.Button(self.panel_main, wx.ID_ANY, "button_14")
        gridsizer_symbol_copy.Add(self.button_14, 0, 0, 0)

        sizer_symbol = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_symbol, 0, wx.EXPAND | wx.TOP, 5)

        self.combobox_symbol = wx.ComboBox(self.panel_main, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_symbol.Add(self.combobox_symbol, 1, 0, 0)

        self.statictext_time = wx.StaticText(self.panel_main, wx.ID_ANY, "1970.01.01 Thu 00:00:00", style=wx.ALIGN_CENTER_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        sizer_symbol.Add(self.statictext_time, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        self.sizer_order = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.sizer_order, 1, wx.BOTTOM | wx.EXPAND | wx.TOP, 10)

        self.orderbutton_bid = widget.OrderButton(self.panel_main, wx.ID_ANY)
        self.sizer_order.Add(self.orderbutton_bid, 3, wx.EXPAND, 0)

        sizer_spread = wx.BoxSizer(wx.VERTICAL)
        self.sizer_order.Add(sizer_spread, 2, wx.EXPAND, 0)

        self.statictext_spread = wx.StaticText(self.panel_main, wx.ID_ANY, "0", style=wx.ALIGN_CENTER_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        self.statictext_spread.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_spread.Add(self.statictext_spread, 1, wx.EXPAND, 0)

        self.spinctrl_spread = wx.SpinCtrl(self.panel_main, wx.ID_ANY, "0", min=0, max=1000000)
        self.spinctrl_spread.SetToolTip("If \"spread > (this value)\",\nyour order will be declined.\n0 means no limit.")
        sizer_spread.Add(self.spinctrl_spread, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self.orderbutton_ask = widget.OrderButton(self.panel_main, wx.ID_ANY)
        self.sizer_order.Add(self.orderbutton_ask, 3, wx.EXPAND, 0)

        sizer_spin = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_spin, 0, wx.EXPAND, 0)

        sizer_lots_slip = wx.BoxSizer(wx.VERTICAL)
        sizer_spin.Add(sizer_lots_slip, 1, wx.EXPAND, 0)

        statictext_lot = wx.StaticText(self.panel_main, wx.ID_ANY, "Lots:")
        sizer_lots_slip.Add(statictext_lot, 0, wx.LEFT, 5)

        self.spinctrldouble_lot = wx.SpinCtrlDouble(self.panel_main, wx.ID_ANY, initial=0.0, min=0.0, max=1000000.0)
        self.spinctrldouble_lot.SetIncrement(0.01)
        self.spinctrldouble_lot.SetDigits(2)
        sizer_lots_slip.Add(self.spinctrldouble_lot, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        statictext_slippage = wx.StaticText(self.panel_main, wx.ID_ANY, "Slippage:")
        sizer_lots_slip.Add(statictext_slippage, 0, wx.LEFT, 5)

        self.spinctrl_slippage = wx.SpinCtrl(self.panel_main, wx.ID_ANY, "0", min=0, max=100)
        sizer_lots_slip.Add(self.spinctrl_slippage, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        self.button_spin = wx.Button(self.panel_main, wx.ID_ANY, "Set Spins")
        self.button_spin.SetToolTip("Set Spread Limit, Lots, Slippage,\nStop Loss and Take Profit.")
        sizer_spin.Add(self.button_spin, 0, wx.EXPAND, 0)

        sizer_sl_tp = wx.BoxSizer(wx.VERTICAL)
        sizer_spin.Add(sizer_sl_tp, 1, wx.EXPAND, 0)

        statictext_sl = wx.StaticText(self.panel_main, wx.ID_ANY, "Stop Loss:")
        sizer_sl_tp.Add(statictext_sl, 0, wx.LEFT, 5)

        self.spinctrl_sl = wx.SpinCtrl(self.panel_main, wx.ID_ANY, "0", min=0, max=1000000)
        sizer_sl_tp.Add(self.spinctrl_sl, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        statictext_tp = wx.StaticText(self.panel_main, wx.ID_ANY, "Take Profit:")
        sizer_sl_tp.Add(statictext_tp, 0, wx.LEFT, 5)

        self.spinctrl_tp = wx.SpinCtrl(self.panel_main, wx.ID_ANY, "0", min=0, max=1000000)
        sizer_sl_tp.Add(self.spinctrl_tp, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        self.panel_main.SetSizer(sizer_main)

        sizer_main.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_connection, self.togglebutton_connect)
        self.Bind(wx.EVT_COMBOBOX, self.on_symbol_selection, self.combobox_symbol)
        self.Bind(wx.EVT_TEXT, self.on_symbol_input, self.combobox_symbol)
        self.Bind(widget.EVT_ORDER, self.on_bid_order, self.orderbutton_bid)
        self.Bind(widget.EVT_ORDER, self.on_ask_order, self.orderbutton_ask)
        self.Bind(wx.EVT_BUTTON, self.on_setting_spin, self.button_spin)
        self.Bind(wx.EVT_CLOSE, self.on_close, self)

    def on_connection(self, event):
        print("Event handler 'on_connection' not implemented!")
        event.Skip()

    def on_symbol_selection(self, event):
        print("Event handler 'on_symbol_selection' not implemented!")
        event.Skip()

    def on_symbol_input(self, event):
        print("Event handler 'on_symbol_input' not implemented!")
        event.Skip()

    def on_bid_order(self, event):
        print("Event handler 'on_bid_order' not implemented!")
        event.Skip()

    def on_ask_order(self, event):
        print("Event handler 'on_ask_order' not implemented!")
        event.Skip()

    def on_setting_spin(self, event):
        print("Event handler 'on_setting_spin' not implemented!")
        event.Skip()

    def on_close(self, event):
        print("Event handler 'on_close' not implemented!")
        event.Skip()


class FrameConfig(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("Config")

        self.panel_main = wx.Panel(self, wx.ID_ANY)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.Add((0, 0), 0, 0, 0)

        self.panel_main.SetSizer(sizer_main)

        sizer_main.Fit(self)
        self.Layout()

