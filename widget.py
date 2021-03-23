import math

import wx
import wx.lib.newevent

# To propagate this event, I use NewCommandEvent() instead of NewEvent().
Order, EVT_ORDER = wx.lib.newevent.NewCommandEvent()

class OrderButton(wx.Panel):
    def __init__(self, parent, id):
        super().__init__(parent, style=wx.BORDER_NONE)
        self.parent = parent

        self.font1 = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')
        self.font2 = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')
        self.font3 = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')
        self.SetForegroundColour('WHITE')

        self.price = 0.00000
        self.update_price(0.00000, 5)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)

    def update_price(self, price, digit):
        price_str = f'{price:.{digit}f}'
        self.price1 = price_str[:-3]
        self.price2 = price_str[-3:-1]
        self.price3 = price_str[-1:]

        if self.price < price:
            self.SetBackgroundColour('RED')
        elif self.price > price:
            self.SetBackgroundColour('BLUE')
        else:
            #self.SetBackgroundColour(wx.NullColour)
            pass

        self.price = price

        self.Refresh()

    def on_paint(self, event):
        dc = wx.PaintDC(self)  # Device Context
        width, height = self.GetSize()

        dc.SetFont(self.font1)
        text_width, text_height = dc.GetTextExtent(self.price1)  # The size which a text takes.
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
        e = Order(event.GetId(), price = self.price)  # EVT_ORDER is generated.
        wx.PostEvent(self.parent, e)

    def on_left_dclick(self, event):
        e = Order(event.GetId(), price = self.price)  # EVT_ORDER is generated.
        wx.PostEvent(self.parent, e)
