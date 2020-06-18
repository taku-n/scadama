from tkinter import *

def main():
    root = Tk()

    root.title('Scadama')

    # root

    frame_order = Frame(root)
    frame_status = Frame(root)
    
    frame_order.pack(side = 'top', expand = True, fill = BOTH)
    frame_status.pack(side = 'bottom', expand = True, fill = BOTH)
    
    # root -> frame_order

    button_bid = Label(frame_order, text = 'button_bid')
    button_ask = Label(frame_order, text = 'button_ask')

    button_bid.pack(side = 'left', expand = True, fill = BOTH)
    button_ask.pack(side = 'right', expand = True, fill = BOTH)

    # root -> frame_status

    label_status = Label(frame_status, text = 'label_status')

    label_status.pack(expand = True, fill = BOTH)

    root.mainloop()

if __name__ == '__main__':
    main()
