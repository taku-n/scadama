(require [libcl [*]])
(import  [libcl [*]])

(import [tkinter [*]])

(setv root (Tk))

;(root.title "Hy")
(.title root "Hy")

; (pack root frame-symbol frame-order)

(Label root)

(root.mainloop)
