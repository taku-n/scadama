from multiprocessing import *
from sys import exit
from time import sleep
from threading import *
from tkinter import *

import MetaTrader5 as mt5

# SETTING
IS_ENABLED_TO_WRITE_A_LOG_FILE = False  # True if you want to write a log file.

class Log:
    is_enabled_to_write_a_log_file = IS_ENABLED_TO_WRITE_A_LOG_FILE
    fd = None

class Ctrl:
    def __init__(self):
        self.is_terminating = False
        self.symbol = None

def main():
    open_log()

    root = Tk()

    root.title('Scadama')

    # root

    frame_order = Frame(root)
    frame_status = Frame(root)
    
    frame_order.pack(side = 'top', expand = True, fill = BOTH)
    frame_status.pack(side = 'bottom', expand = True, fill = BOTH)
    
    # root -> frame_order

    button_bid = Button(frame_order)
    button_ask = Button(frame_order)

    button_bid.pack(side = 'left', expand = True, fill = BOTH)
    button_ask.pack(side = 'right', expand = True, fill = BOTH)

    # root -> frame_status

    label_status = Label(frame_status)

    label_status.pack(expand = True, fill = BOTH)

    # Connect to a MetaTrader 5.

    label_status.configure(text = 'Connecting to a MetaTrader 5...')
    if not mt5.initialize():
        write_log('MetaTrader5.initialize() failed.')
        mt5.shutdown()
        close_log()
        exit()

    write_log('Writing MetaTrader5.version()...')
    write_log(mt5.version())
    write_log('Writing MetaTrader5.terminal_info()...')
    write_log(mt5.terminal_info())
    write_log('Writing MetaTrader5.account_info()...')
    write_log(mt5.account_info())

    # Dont use bidirectional pipes (Pipe(True)) because they seem unstable.
    write_log('Opening pipes...')
    pipe_tick_rx, pipe_tick_tx = Pipe(False)  # Interprocess Communication for ticks.
    pipe_ctrl_rx, pipe_ctrl_tx = Pipe(False)  # Interprocess Communication for controling a process.

    write_log('Starting a thread...')
    thread = Thread(target = recv_tick, args = (pipe_tick_rx, button_bid, button_ask))
    thread.start()

    write_log('Starting a process...')
    process = Process(target = send_tick, args = (pipe_tick_tx, pipe_ctrl_rx))
    process.start()

    ctrl = Ctrl()
    ctrl.symbol = 'EURUSD'
    pipe_ctrl_tx.send(ctrl)

    write_log('Starting the mainloop...')
    root.mainloop()

    # The main window is closed.

    write_log('Terminating the child process...')
    ctrl.is_terminating = True
    pipe_ctrl_tx.send(ctrl)
    process.terminate()  # Kill the child process.
    process.join()       # Wait to finish killing.

    write_log('Closing the pipes...')
    pipe_tick_rx.close()
    pipe_tick_tx.close()
    pipe_ctrl_rx.close()
    pipe_ctrl_tx.close()

    write_log('Shutting down the MetaTrader5 connection...')
    sleep(1)
    mt5.shutdown()
    sleep(1)

    write_log('Closing the log...')
    close_log()
    sleep(1)

def open_log():
    if Log.is_enabled_to_write_a_log_file:
        Log.fd = open('log.txt', 'w')

def write_log(msg):
    if Log.is_enabled_to_write_a_log_file:
        Log.fd.write(msg)
    else:
        print(msg)

def close_log():
    if Log.is_enabled_to_write_a_log_file:
        Log.fd.close()

def recv_tick(pipe, button_bid, button_ask):  # Runs in a thread.
    tick = None

    while True:
        try:
            tick = pipe.recv()
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            exit()

        write_log('Rewriting a tick...')
        button_bid.configure(text = tick)

def send_tick(pipe, pipe_ctrl):  # Runs in a process.
    write_log('Initializing MetaTrader5 in send_tick()...')
    if not mt5.initialize():
        #pipe.send('MetaTrader5.initialize() in send_tick() failed.') as a dictionary?
        mt5.shutdown()
        exit()

    ctrl = None

    thread = Thread(target = send_tick_ctrl, args = (pipe_ctrl, mt5, ctrl))
    thread.start()

    try:
        ctrl = pipe_ctrl.recv()
    except Exception as e:
        if e.args != ():
            write_log(e.args)
        exit()

    tick = None

    while True:
        write_log('Polling data of ctrl...')
        try:
            if pipe_ctrl.poll():
                write_log('Getting data of ctrl...')
                ctrl = pipe_ctrl.recv()
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            exit()

        write_log('ctrl:')
        write_log(ctrl)
        write_log('ctrl.is_terminating:')
        write_log(ctrl.is_terminating)
        write_log('ctrl.symbol:')
        write_log(ctrl.symbol)

        if ctrl.is_terminating:
            mt5.shutdown()
            sleep(1)
            exit()

        write_log('Getting a tick...')
        tick = mt5.symbol_info_tick(ctrl.symbol)._asdict()

        try:
            pipe.send(tick)
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            exit()

        sleep(0.001)

def send_tick_ctrl(pipe_ctrl, mt5, ctrl):  # Runs in a thread of a child process.
    pass

# UNIX like OSes dont need to check if the module is __main__ but for Windows, it is essential.
# Since Windows doesnt have the fork system call,
# child processes run their program from the first line like their parent process does.
if __name__ == '__main__':
    freeze_support()  # Windows Only needs this line.
    main()

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
