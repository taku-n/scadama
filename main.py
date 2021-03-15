from multiprocessing import *
import os

import wx

import impl

class AppMain(wx.App):
    def OnInit(self):
        self.frame_main_impl = impl.FrameMainImpl(None, wx.ID_ANY, title = 'Scadama')
        self.SetTopWindow(self.frame_main_impl)
        self.frame_main_impl.Show()

        return True

def main():
    app_main = AppMain(0)
    app_main.MainLoop()

# To process concurrently,
# UNIX like OSes do not need to check if the module is __main__ but for Windows, it is essential.
# Since Windows does not have the fork system call,
# child processes run their program from the first line like their parent process does.
if __name__ == '__main__':
    freeze_support()  # To produce an executable. Only Windows needs this line.

    main()

    # Without this line, you can not back to your command prompt.
    # Without this line, maybe one or two processes keep alive but I can not figure out.
    os._exit(1)

# RuntimeError:
#         An attempt has been made to start a new process before the
#         current process has finished its bootstrapping phase.
#
#         This probably means that you are not using fork to start your
#         child processes and you have forgotten to use the proper idiom
#         in the main module:
#
#             if __name__ == '__main__':
#                 freeze_support()
#                 ...
#
#         The "freeze_support()" line can be omitted if the program
#         is not going to be frozen to produce an executable.
