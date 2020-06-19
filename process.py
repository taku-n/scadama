import datetime
import multiprocessing
import queue
import threading
import time

# Open an elevated command prompt. (コマンド プロンプト を 管理者として実行)
# >pip install pywin32
# >git clone https://github.com/mhammond/pywin32.git
# >python pywin32/pywin32_postinstall.py -install
#
# To check the installation, open a python interpreter.
# >>> import pythoncom
# >>> print(pythoncom.__file__)
# Check if C:\WINDOWS\SYSTEM32\pythoncom38.dll shows.
# >>> dir(pythoncom)
# Check if its functions shows.
import pythoncom

import wmi

def main():
    print('Press Q then Enter, this program ends after a while.')

    q_creation = queue.Queue()
    q_deletion = queue.Queue()

    thread_creation = threading.Thread(target = creation, args = (q_creation, ))
    thread_deletion = threading.Thread(target = deletion, args = (q_deletion, ))

    thread_creation.start()
    thread_deletion.start()

    while True:
        x = input()  # Blocking

        if x == 'q':
            break
    
    q_creation.put('creation() take a poison pill.')
    q_deletion.put('deletion() take a poison pill.')

    thread_creation.join()
    thread_deletion.join()

def creation(q):
    pythoncom.CoInitialize()
    w = wmi.WMI()

    process_watcher_creation = w.Win32_Process.watch_for('creation')

    while True:
        if not q.empty():
            print(q.get())
            break

        created_process = process_watcher_creation()  # Blocking
        print(datetime.datetime.now(), created_process.Caption, 'is created.')

    pythoncom.CoUninitialize()

def deletion(q):
    pythoncom.CoInitialize()
    w = wmi.WMI()

    process_watcher_deletion = w.Win32_Process.watch_for('deletion')

    while True:
        if not q.empty():
            print(q.get())
            break

        deleted_process = process_watcher_deletion()  # Blocking
        print(datetime.datetime.now(), deleted_process.Caption, 'is deleted.')

    pythoncom.CoUninitialize()

if __name__ == '__main__':
    main()
