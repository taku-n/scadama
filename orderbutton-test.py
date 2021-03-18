import wx

import widget

class FrameTest(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetTitle("OrderButton Widget Test")

        panel = wx.Panel(self)

        boxsizer_main = wx.BoxSizer(wx.VERTICAL)
        boxsizer_order = wx.BoxSizer(wx.HORIZONTAL)

        self.orderbutton = widget.OrderButton(panel)

        boxsizer_order.Add(self.orderbutton, 1, wx.EXPAND)
        boxsizer_main.Add(boxsizer_order, 1, wx.EXPAND)

        panel.SetSizer(boxsizer_main)

def main():
    app = wx.App()  # The wx.App object must be created first!

    frame_test = FrameTest(None)
    frame_test.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
