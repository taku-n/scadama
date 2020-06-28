import datetime
from functools import partial
from multiprocessing import *
import os
import sys
from time import sleep
from threading import *
from tkinter import *
import tkinter.ttk as ttk

import MetaTrader5 as mt5

# SETTING
IS_ENABLED_TO_WRITE_A_LOG_FILE = False  # True if you want to write a log file.

class Log:
    is_enabled_to_write_a_log_file = IS_ENABLED_TO_WRITE_A_LOG_FILE
    fd = None

class Symbols:
    total = 0
    symbols = []
    infos = {}
    selection = ''

class Ctrl:
    def __init__(self):
        self.is_terminating = False
        self.symbol = None

class Tick:  # This is set every time recv_tick() receives a tick.
    symbol = ''
    bid = 0.0
    ask = 0.0
    spread = 0.0
    spread_max = 0.0

class Symbol:  # A class for a process to send a tick.
    symbol = ''

def main():
    open_log()

    root = Tk()

    root.title('Scadama')

    # root

    frame_symbol = Frame(root)
    frame_order = Frame(root)
    frame_close = Frame(root)
    frame_status = Frame(root)
    
    frame_symbol.pack(side = TOP, expand = True, fill = BOTH)
    frame_order.pack(side = TOP, expand = True, fill = BOTH)
    frame_close.pack(side = TOP, expand = True, fill = BOTH)
    frame_status.pack(side = TOP, expand = True, fill = BOTH)

    # root -> frame_symbol

    combobox_symbol = ttk.Combobox(frame_symbol, state = 'readonly')
    label_time = Label(frame_symbol)

    combobox_symbol.pack(side = LEFT, expand = True, fill = BOTH)
    label_time.pack(side = LEFT, expand = True, fill = BOTH)

    # root -> frame_order

    button_bid = Button(frame_order, command = partial(order, 'BID'))
    button_ask = Button(frame_order, command = partial(order, 'ASK'))
    spinbox_spread_value = DoubleVar(value = 0.0)
    spinbox_spread_value.trace('w', partial(spinbox_spread_value_changed, spinbox_spread_value))
    spinbox_spread = Spinbox(frame_order, textvariable = spinbox_spread_value,
            from_ = 0.0, increment = 0.1, to = 1000000.0, format = '%.1f')
    label_spread = Label(frame_order)

    button_bid.pack(side = LEFT, expand = True, fill = BOTH)
    button_ask.pack(side = RIGHT, expand = True, fill = BOTH)
    spinbox_spread.pack(side = TOP, expand = True, fill = BOTH)
    label_spread.pack(side = BOTTOM, expand = True, fill = BOTH)

    # root -> frame_status

    label_status = Label(frame_status)

    label_status.pack(expand = True, fill = BOTH)

    # Connect to a MetaTrader 5.

    label_status.configure(text = 'Connecting to a MetaTrader 5...')
    if not mt5.initialize():
        write_log('MetaTrader5.initialize() failed.')
        mt5.shutdown()
        close_log()
        sys.exit()

    write_log('Writing MetaTrader5.version()...')
    write_log(mt5.version())
    write_log('Writing MetaTrader5.terminal_info()...')
    write_log(mt5.terminal_info())
    write_log('Writing MetaTrader5.account_info()...')
    write_log(mt5.account_info())

    Symbols.total = mt5.symbols_total()
    for symbol in mt5.symbols_get():
        Symbols.symbols.append(symbol.name)
        Symbols.infos[symbol.name] = symbol
    print('total:', Symbols.total)
    print('symbols:', Symbols.symbols)
    print('infos:', Symbols.infos)

    combobox_symbol.configure(values = Symbols.symbols)
    combobox_symbol.current(0)  # The initial value of the Combobox.
    Symbols.selection = combobox_symbol.get()
    combobox_symbol.bind('<<ComboboxSelected>>', partial(symbol_changed, combobox_symbol))

    # Dont use bidirectional pipes (Pipe(True)) because they seem unstable.
    write_log('Opening pipes...')
    pipe_tick_rx, pipe_tick_tx = Pipe(False)  # Interprocess Communication for ticks.
    pipe_ctrl_rx, pipe_ctrl_tx = Pipe(False)  # Interprocess Communication for controling a process.

    # A thread to receive a tick.
    write_log('Starting a thread...')
    thread = Thread(target = recv_tick, args = (pipe_tick_rx, label_time, button_bid, button_ask, label_spread))
    thread.start()

    # A process to send a tick.
    write_log('Starting a process...')
    process = Process(target = send_tick_ctrl, args = (pipe_ctrl_rx, pipe_tick_tx))
    process.start()

    ctrl = Ctrl()
    ctrl.symbol = Symbols.symbols[0]
    pipe_ctrl_tx.send(ctrl)
    Tick.symbol = Symbols.symbols[0]

    write_log('Starting the mainloop...')
    root.mainloop()

    # The main window is closed. Termination.

    write_log('Terminating the child process...')
    ctrl.is_terminating = True
    pipe_ctrl_tx.send(ctrl)
    sleep(1)             # Wait for MetaTrader5.shutdown() in send_tick_ctrl().
    process.terminate()  # Kill the child process.
    process.join()       # Wait to finish killing.

    write_log('Closing the pipes...')
    pipe_tick_rx.close()
    pipe_tick_tx.close()
    pipe_ctrl_rx.close()
    pipe_ctrl_tx.close()

    write_log('Shutting down the MetaTrader5 connection...')
    mt5.shutdown()

    write_log('Closing the log...')
    close_log()

    print('The program ends.')

def symbol_changed(combobox, event):
    Symbols.selection = combobox.get()
    print(Symbols.selection)

def order(type):
    if type == 'ASK':
        print('ask!')
    elif type == 'BID':
        print('bid!')
    else:
        print('invalid!')

def spinbox_spread_value_changed(*args):
    try:
        spread_max = args[0].get()
    except Exception as e:
        if e.args != ():
            write_log(e.args)
        Tick.spread_max = 0.0
        return

    if spread_max < 0.0:  # (0.0 == -0.0): True, (0.0 is -0.0): False
        Tick.spread_max = 0.0
    elif 1000000.0 < spread_max:
        Tick.spread_max = 1000000.0
    else:
        Tick.spread_max = spread_max

def open_log():
    if Log.is_enabled_to_write_a_log_file:
        Log.fd = open('log.txt', 'w')

def write_log(msg):
    if Log.is_enabled_to_write_a_log_file:
        Log.fd.write(f'{msg}\n')
    else:
        print(msg)

def close_log():
    if Log.is_enabled_to_write_a_log_file:
        Log.fd.close()

def send_error(pipe, msg):
    try:
        pipe.send({'error': msg})
    except:
        pass

def send_info(pipe, msg):
    try:
        pipe.send({'info': msg})
    except:
        pass

def recv_tick(pipe, label_time, button_bid, button_ask, label_spread):  # Runs in a thread.
    while True:
        # Get a tick.

        try:
            tick = pipe.recv()
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        write_log(tick)

        # Show the servers local time.

        try:
            time = tick['time']
        except Exception as e:
            if e.args != ():
                write_log(f'Error, getting a time: {e.args}')
            sys.exit()

        # This doesnt mean it is UTC but a servers local time.
        time_zone = datetime.timezone(datetime.timedelta(hours = 0))

        time = datetime.datetime.fromtimestamp(time, time_zone)
        time = f'{time:%Y.%m.%d %a %H:%M:%S}'  # f-string

        try:
            label_time.configure(text = time)
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        # Show ask, bid and spread.

        try:
            ask = tick['ask']
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        Tick.ask = ask

        try:
            bid = tick['bid']
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        Tick.bid = bid

        spread = (ask - bid) * 10000.0
        Tick.spread = spread

        try:
            button_ask.configure(text = f'{ask:.5f}')
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        try:
            button_bid.configure(text = f'{bid:.5f}')
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

        try:
            label_spread.configure(text = f'{spread:.1f}')
        except Exception as e:
            if e.args != ():
                write_log(e.args)
            sys.exit()

def send_tick_ctrl(pipe_ctrl, pipe):  # Runs in a child process.
    if not mt5.initialize():
        send_error(pipe, 'MetaTrader5.initialize() in send_tick_ctrl() failed.')
        mt5.shutdown()
        sys.exit()

    ctrl = None

    try:
        ctrl = pipe_ctrl.recv()  # Blocking until this gets a first control signal.
    except:
        sys.exit()

    thread = Thread(target = send_tick, args = (pipe, mt5, ctrl))
    thread.start()

    while True:
        try:
            ctrl = pipe_ctrl.recv()
        except:
            sys.exit()

        if ctrl.is_terminating:
            mt5.shutdown()

            # BUG:
            # I dont know why but this information is not received
            # when you close this application
            # with clicking the top left icon of its window, waiting for a while and clicking Close in the menu.
            # Ofcourse this information doesnt show.
            # This problem occurs too when you run this program for a long time.
            send_info(pipe, 'MetaTrader5.shutdown() in send_tick_ctrl() ends.')

            sys.exit()

def send_tick(pipe, mt5, ctrl):  # Runs in a thread of a child process.
    last_tick = None

    while True:
        try:
            tick = mt5.symbol_info_tick(ctrl.symbol)._asdict()  # Non-blocking
        except Exception as e:
            if e.args != ():
                send_error(pipe, e.args)
            sys.exit()

        if tick != last_tick:
            try:
                pipe.send(tick)
            except:
                sys.exit()

        last_tick = tick
        sleep(0.001)

# To process concurrently,
# UNIX like OSes dont need to check if the module is __main__ but for Windows, it is essential.
# Since Windows doesnt have the fork system call,
# child processes run their program from the first line like their parent process does.
if __name__ == '__main__':
    freeze_support()  # Windows Only needs this line.
    main()

    # Without this line, you cant back to your command prompt.
    # Without this line, maybe one or two processes keep alive but i cant figure out.
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
