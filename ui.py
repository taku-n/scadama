# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Fri Mar 19 02:08:43 2021
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

        sizer_symbol = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_symbol, 0, wx.EXPAND, 0)

        self.combobox_symbol = wx.ComboBox(self.panel_main, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_symbol.Add(self.combobox_symbol, 1, 0, 0)

        statictext_time = wx.StaticText(self.panel_main, wx.ID_ANY, "1970.01.01 Thu 00:00:00")
        sizer_symbol.Add(statictext_time, 0, 0, 0)

        gridsizer_symbol = wx.GridSizer(2, 3, 0, 0)
        sizer_main.Add(gridsizer_symbol, 0, wx.EXPAND, 0)

        self.button_3 = wx.Button(self.panel_main, wx.ID_ANY, "button_3")
        gridsizer_symbol.Add(self.button_3, 0, 0, 0)

        self.button_4 = wx.Button(self.panel_main, wx.ID_ANY, "button_4")
        gridsizer_symbol.Add(self.button_4, 0, 0, 0)

        self.button_5 = wx.Button(self.panel_main, wx.ID_ANY, "button_5")
        gridsizer_symbol.Add(self.button_5, 0, 0, 0)

        self.button_6 = wx.Button(self.panel_main, wx.ID_ANY, "button_6")
        gridsizer_symbol.Add(self.button_6, 0, 0, 0)

        self.button_7 = wx.Button(self.panel_main, wx.ID_ANY, "button_7")
        gridsizer_symbol.Add(self.button_7, 0, 0, 0)

        self.button_8 = wx.Button(self.panel_main, wx.ID_ANY, "button_8")
        gridsizer_symbol.Add(self.button_8, 0, 0, 0)

        self.sizer_order = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.sizer_order, 1, wx.EXPAND | wx.TOP, 10)

        self.orderbutton_bid = widget.OrderButton(self.panel_main, wx.ID_ANY)
        self.sizer_order.Add(self.orderbutton_bid, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_order.Add(sizer_2, 1, wx.EXPAND, 0)

        self.spinctrldouble_spread = wx.SpinCtrlDouble(self.panel_main, wx.ID_ANY, initial=0, min=0.0, max=1000000.0)
        self.spinctrldouble_spread.SetIncrement(0.1)
        self.spinctrldouble_spread.SetDigits(1)
        sizer_2.Add(self.spinctrldouble_spread, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 10)

        self.statictext_spread = wx.StaticText(self.panel_main, wx.ID_ANY, "0.0")
        sizer_2.Add(self.statictext_spread, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.orderbutton_ask = widget.OrderButton(self.panel_main, wx.ID_ANY)
        self.sizer_order.Add(self.orderbutton_ask, 1, wx.EXPAND, 0)

        self.panel_main.SetSizer(sizer_main)

        sizer_main.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_connection, self.togglebutton_connect)

    def on_connection(self, event):
        print("Event handler 'on_connection' not implemented!")
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

