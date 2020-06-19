from tkinter import *

def main():
    root = Tk()

    root.title('Scadama')

    # root

    frame_time = Frame(root)
    frame_order = Frame(root)
    frame_close = Frame(root)
    frame_status = Frame(root)

    frame_time.pack(side = TOP, expand = True, fill = BOTH)
    frame_order.pack(side = TOP, expand = True, fill = BOTH)
    frame_close.pack(side = TOP, expand = True, fill = BOTH)
    frame_status.pack(side = TOP, expand = True, fill = BOTH)

    # root -> frame_time

    create_label(frame_time, 'label_time', LEFT)

    # root -> frame_order

    create_label(frame_order, 'button_bid', LEFT)
    create_label(frame_order, 'button_ask', RIGHT)
    create_label(frame_order, 'spinbox_spread', TOP)
    create_label(frame_order, 'label_spread', BOTTOM)

    # root -> frame_close

    create_label(frame_close, 'button_close_bid', LEFT)
    create_label(frame_close, 'button_close', LEFT)
    create_label(frame_close, 'button_close_ask', LEFT)

    # root -> frame_status

    create_label(frame_status, 'label_status', TOP)

    root.mainloop()

def create_label(frame, text, side):
    label = Label(frame, text = text)
    label.pack(side = side, expand = True, fill = BOTH)

if __name__ == '__main__':
    main()
