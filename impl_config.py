import ui

class FrameConfigImpl(ui.FrameConfig):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.Show()
