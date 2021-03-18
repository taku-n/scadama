import math

import wx

class OrderButton(wx.Panel):
    def __init__(self, parent, id):
        super().__init__(parent, style=wx.BORDER_NONE)

        self.font1 = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')
        self.font2 = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')
        self.font3 = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')

        self.price = 0.00000
        self.update_price(0.00000, 'USD')

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)

    def update_price(self, price, currency_profit):  # e.g. EURUSD, USD is the currency_profit.
        if currency_profit == 'USD':
            price_str = format(price, '.5f')
            self.price1 = price_str[:-3]
            self.price2 = price_str[-3:-1]
            self.price3 = price_str[-1:]
        elif currency_profit == 'JPY':
            price_str = format(price, '.3f')
            self.price1 = price_str[:-3]
            self.price2 = price_str[-3:-1]
            self.price3 = price_str[-1:]
        else:
            self.price1 = ''
            self.price2 = 'NA'
            self.price3 = ''

        if self.price < price:
            self.SetBackgroundColour('RED')
        elif self.price > price:
            self.SetBackgroundColour('BLUE')
        else:
            self.SetBackgroundColour(wx.NullColour)

        self.price = price

        self.Refresh()

    def on_paint(self, event):
        dc = wx.PaintDC(self)  # Device Context
        width, height = self.GetSize()

        dc.SetFont(self.font1)
        text_width, text_height = dc.GetTextExtent(self.price1)
        dc.DrawText(self.price1,
                math.floor(width / 6 - text_width / 2), math.floor(height - text_height))

        dc.SetFont(self.font2)
        text_width, text_height = dc.GetTextExtent(self.price2)
        dc.DrawText(self.price2,
                math.floor((width / 6) * 3 - text_width / 2),
                math.floor(height / 2 - text_height / 2))

        dc.SetFont(self.font3)
        text_width, text_height = dc.GetTextExtent(self.price3)
        dc.DrawText(self.price3, math.floor((width / 6) * 5 - text_width / 2), 0)

    def on_size(self, event):
        self.Refresh()

    def on_left_down(self, event):
        pass

    def on_left_dclick(self, event):
        self.on_left_down(event)
