(require [libcl [*]])
(import  [libcl [*]])

(import [tkinter [*]])

(defmacro tk [name &optional [title "tk"] &rest body]
  `(do (setv ~name (Tk))
       (.title ~name ~title)
       ~@body))

(tk root "hello")

;(setv root (Tk))

;(root.title "Hy")
;(.title root "Hy")

; (pack root frame-symbol frame-order)
; frame マクロ, label マクロ, button マクロ, ... みたいなのがいい気がしてきた
; いきなり全体はムリなのでそれぞれの部品のマクロをつくってみる

(setv label_hello (Label root :text "hello, world"))
(.pack label_hello :side LEFT :expand True :fill BOTH)

(root.mainloop)
