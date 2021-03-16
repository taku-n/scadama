import MetaTrader5 as mt5
import toml

import ui

class FrameMainImpl(ui.FrameMain):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        config = toml.load(open('config.toml'))

        # choice_client

        client = config['client']

        for x in client:
            self.choice_client.Append(x)

        self.choice_client.SetSelection(0)

        # MetaTrader5

        print('MetaTrader5 package version:', mt5.__version__)
        print('MetaTrader5 package author:', mt5.__author__)

    def connect(self, event):
        client = self.choice_client.GetStringSelection()

        if self.togglebutton_connect.GetValue():  # Pressed
            if mt5.initialize(client):
                self.choice_client.Disable()
                self.togglebutton_connect.SetLabel('Disconnect')
                print('Connected to', client)
                print('Terminal Info:', mt5.terminal_info())
                print('MetaTrader 5 version:', mt5.version())
            else:
                self.togglebutton_connect.SetValue(False)
                print('Failed to connect to', client)
        else:  # Pulled
            mt5.shutdown()
            print('Disconnected from', client)
            self.choice_client.Enable()
            self.togglebutton_connect.SetLabel('Connect')

        event.Skip()
