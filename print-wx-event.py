import wx

def main():
    for x in dir(wx):
        if x.startswith('EVT'):
            print(x)

if __name__ == '__main__':
    main()
